from djoser.views import UserViewSet
from rest_framework import exceptions, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.models import Subscription, User
from users.pagination import CustomPagination
from users.serializers import CustomUserSerializer, SubscriptionSerializer


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
        user_subscriptions = user.following.all()
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
        subscription = Subscription.objects.get_or_create(
            user=subscriber, author=author
        )
        if request.method == 'POST':
            serializer = SubscriptionSerializer(subscription[0])
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        if request.method == 'DELETE':
            if not subscriber.following.exists():
                raise exceptions.ValidationError(
                    detail='У вас нет подписки на этого автора!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            subscription[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
