from datetime import datetime

from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeCreateUpdateSerializer,
    FavoriteRecipeSerializer,
    ShoppingListSerializer,
)
from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    IngredientAmount,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in permissions.SAFE_METHODS:
            return RecipeListSerializer
        return RecipeCreateUpdateSerializer

    def action_post_delete(self, pk, serializer_class):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        model_obj = serializer_class.Meta.model.objects.filter(
            user=user,
            recipe=recipe,
        )

        if self.request.method == 'POST':
            serializer = serializer_class(
                data={'user': user.id, 'recipe': pk},
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not model_obj.exists():
                return Response(
                    {'error': 'Этого рецепта нет в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        return self.action_post_delete(pk, FavoriteRecipeSerializer)

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return self.action_post_delete(pk, ShoppingListSerializer)

    @action(
            methods=['GET'],
            detail=False,
            permission_classes=(permissions.IsAuthenticated,),
            pagination_class=None,
    )
    def download_shopping_cart(self, request):
        """
        Функция для добавления рецептов в список покупок.
        Доступ для авторизованных.
        """
        user = request.user
        if not user.shopping_list.exists():
            return Response(
                {'error': 'Список покупок пуст'},
                status=status.HTTP_204_NO_CONTENT
            )
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_list__user=user
        ).values(
            ingredients=models.F('ingredient__name'),
            measure=models.F('ingredient__measurement_unit')
        ).annotate(amount=models.Sum('amount'))

        filename = f'{user.username}_shopping_list.txt'
        shopping_list = (f'Список покупок\n\n{user.username}\n'
                         f'{datetime.now().strftime("%d/%m/%Y %H:%M")}\n\n')
        for ing in ingredients:
            shopping_list += (
                f'{ing["ingredients"]} - {ing["amount"]}, {ing["measure"]}\n'
            )
        response = HttpResponse(shopping_list,
                                content_type='text.txt; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
