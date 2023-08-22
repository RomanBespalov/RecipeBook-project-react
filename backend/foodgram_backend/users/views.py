from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Subscribe, User
from users.serializers import (
    CustomUserSerializer,
    SubscribeSerializer,
)


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет для работы с пользователями. Доступно для всех.
    Обработка запросов на создание и получение пользователей.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)
    add_serializer = SubscribeSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        """
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        Доступ для авторизванных. Разрешен метод GET.
        """
        user = self.request.user
        authors = User.objects.filter(followers__user=user)
        page = self.paginate_queryset(authors)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        """
        Разрешены методы POST, DELETE, подписка и отписка от автора.
        Доступ для авторизованных.
        """
        user = self.request.user
        author = get_object_or_404(User, id=id)
        subscription = Subscribe.objects.filter(user=user, author=author)

        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    {'error': 'Вы уже подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SubscribeSerializer(
                author, context={'request': request}
            )
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {'error': 'Вы не подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
