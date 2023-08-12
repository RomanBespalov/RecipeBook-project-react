from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    TagsViewSet,
    RecipeViewSet,
    IngredientsViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('users/', include('users.urls')),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
