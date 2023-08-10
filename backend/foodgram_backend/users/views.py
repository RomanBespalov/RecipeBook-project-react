from djoser.views import UserViewSet

from users.models import User
from users.serializers import (
    CustomUserCreateSerializer,
    CustomUserListSerializer
)
from djoser.serializers import SetPasswordSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        return CustomUserListSerializer
