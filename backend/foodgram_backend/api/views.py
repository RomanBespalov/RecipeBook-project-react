from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions, status, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.pagination import CustomPagination
from django.db import models
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Tag, Recipe, Favorite, Ingredient, ShoppingCart, RecipeIngredient
from api.serializers import (
    TagSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    IngredientSerializer
)
from api.filters import IngredientSearchFilter, RecipeFilter


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)
    permission_classes = (permissions.AllowAny,)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipeingredient_set__ingredient', 'tags'
        ).all()
        return recipes

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            if Favorite.objects.filter(recipe=recipe, user=user).exists():
                raise exceptions.ValidationError(
                    detail='Рецепт уже есть в избранном!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(recipe=recipe, user=user)
            serializer = FavoriteSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        if request.method == "DELETE":
            if not Favorite.objects.filter(recipe=recipe, user=user).exists():
                raise exceptions.ValidationError(
                    detail='Рецепта не было в избранном!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            favorite_recipe = get_object_or_404(
                Favorite, recipe=recipe, user=user
            )
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
                raise exceptions.ValidationError(
                    detail='Рецепт уже есть в списке покупок!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(recipe=recipe, user=user)
            serializer = FavoriteSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if request.method == "DELETE":
            if not ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
                raise exceptions.ValidationError(
                    detail='Рецепта не было в списке покупок!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            shopping_cart = ShoppingCart.objects.filter(recipe=recipe, user=user)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(
                    amount=models.Sum('amount')
                )
        data = ingredients.values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        shopping_cart = 'Список покупок:\n'
        for name, measure, amount in data:
            shopping_cart += (f'{name.capitalize()} {amount} {measure},\n')
        return HttpResponse(shopping_cart, content_type='text/plain')
