from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    TagViewSet,
    RecipeViewSet,
    IngredientViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('users/', include('users.urls')),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
