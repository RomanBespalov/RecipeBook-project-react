from djoser.views import UserViewSet
from users.models import User, Subscription
from users.serializers import CustomUserSerializer, SubscriptionSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(user_subscriptions, many=True)
        return Response(serializer.data)
