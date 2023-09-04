from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.pagination import CustomPagination
from django.db import models
from django.http import HttpResponse

from recipes.models import Tag, Recipe, Favorite, Ingredient, ShoppingCart, RecipeIngredient
from api.serializers import (
    TagSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    IngredientSerializer
)


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination

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
            Favorite.objects.create(recipe=recipe, user=user)
            serializer = FavoriteSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == "DELETE":
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
            ShoppingCart.objects.create(recipe=recipe, user=user)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data)

        if request.method == "DELETE":
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
