from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Subscribe, User


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения сведений о рецепте."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class CustomUserSerializer(UserSerializer):
    """Сериализатор для отображения информации о пользователе."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj.id).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления, удаления и просмотра подписок."""
    recipes = ShortRecipeSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = (
            *CustomUserSerializer.Meta.fields,
            'recipes',
            'recipes_count'
        )
        read_only_fields = ('__all__',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj.id).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для отображения данных после регистрации."""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("email", "id", "username", "first_name",
                  "last_name", "password")
