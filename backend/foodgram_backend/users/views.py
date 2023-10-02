from djoser.views import UserViewSet
from rest_framework import exceptions, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.models import Subscription, User
from users.pagination import CustomPagination
from users.serializers import (CustomUserSerializer, SubscribeSerializer,
                               SubscriptionSerializer)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, serializer):
        user = self.request.user
        user_subscriptions = user.follower.all()
        pages = self.paginate_queryset(user_subscriptions)
        serializer = SubscriptionSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id):
        subscriber = self.request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            data = {
                'user': subscriber.id,
                'author': author.id,
            }
            serializer = SubscribeSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not subscriber.follower.filter(author=author).exists():
                raise exceptions.ValidationError(
                    detail='У вас нет подписки на этого автора!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            subscription = get_object_or_404(
                Subscription,
                user=subscriber,
                author=author,
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
