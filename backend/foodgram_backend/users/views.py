from rest_framework import permissions
from djoser.views import UserViewSet

from users.models import User
from users.serializers import UserListSerializer, UserCreateSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'list':
            return UserListSerializer
