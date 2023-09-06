from djoser.views import UserViewSet
from users.models import User, Subscription
from users.pagination import CustomPagination
from users.serializers import CustomUserSerializer, SubscriptionSerializer
from rest_framework import permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, serializer):
        user = self.request.user
        user_subscriptions = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(user_subscriptions)
        serializer = SubscriptionSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id):
        subscriber = self.request.user
        author = get_object_or_404(User, id=id)
        if request.method == "POST":
            if subscriber == author:
                raise exceptions.ValidationError(
                    detail='Нельзя подписаться на себя!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            if Subscription.objects.filter(user=subscriber, author=author).exists():
                raise exceptions.ValidationError(
                    detail='Вы уже подписаны на этого автора!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            subscription = Subscription.objects.create(user=subscriber, author=author)
            serializer = SubscriptionSerializer(subscription)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                )
        if request.method == "DELETE":
            if not Subscription.objects.filter(user=subscriber, author=author).exists():
                raise exceptions.ValidationError(
                    detail='У вас нет подписки на этого автора!',
                    code=status.HTTP_400_BAD_REQUEST,
                )
            subscription = Subscription.objects.filter(user=subscriber, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
