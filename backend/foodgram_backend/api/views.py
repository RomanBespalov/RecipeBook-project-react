from rest_framework import viewsets

from recipes.models import (
    Tags,
    Recipe,
    Ingredients,
)
from api.serializers import (
    TagsSerializer,
    RecipeSerializer,
    IngredientsSerializer,
)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
