from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import exceptions, serializers, status

from recipes.models import Recipe
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.follower.filter(author=obj).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'password',
        )


class RecipeSubscriptionField(serializers.Field):
    """Сериализатор для вывода рецептов в подписках."""

    def get_attribute(self, instance):
        return Recipe.objects.filter(author=instance.author)

    def to_representation(self, recipes_list):
        recipes_data = []
        for recipes in recipes_list:
            recipes_data.append(
                {
                    'id': recipes.id,
                    'name': recipes.name,
                    'image': recipes.image.url,
                    'cooking_time': recipes.cooking_time,
                }
            )
        return recipes_data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Cериализатор создания подписок."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSubscriptionField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
            'recipes', 'recipes_count',
        )

    def get_is_subscribed(self, obj):
        if obj.user.is_authenticated:
            return Subscription.objects.filter(
                user=obj.user, author=obj.author
            ).exists()
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        subscriber = data['user']
        author = data['author']
        if subscriber == author:
            raise exceptions.ValidationError(
                detail='Нельзя подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if subscriber.following.filter(author=author).exists():
            raise exceptions.ValidationError(
                detail='Вы уже подписаны на этого автора!',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
