from djoser.views import UserViewSet
from users.models import User, Subscription
from users.pagination import CustomPagination
from users.serializers import CustomUserSerializer, SubscriptionSerializer, SubscriptionCreateSerializer
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)
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
        if request.method == "POST":
            subscriber = self.request.user
            author = get_object_or_404(User, id=id)
            subscription = Subscription.objects.create(user=subscriber, author=author)
            serializer = SubscriptionCreateSerializer(subscription)
            return Response(serializer.data)
        if request.method == "DELETE":
            subscriber = self.request.user
            author = get_object_or_404(User, id=id)
            subscription = Subscription.objects.filter(user=subscriber, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
