from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# app_name = 'api'

# router_v1 = DefaultRouter()

from api.views import index

urlpatterns = [
    path('index', index),
    # path('', include(router_v1.urls)),
    # path('users/', include('users.urls')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]
