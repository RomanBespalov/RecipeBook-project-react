from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

from users.models import User


UNIT_CHOICES = [
    ('г', 'грамм'),
    ('кг', 'килограмм'),
    ('мл', 'миллилитр'),
    ('л', 'литр'),
    ('шт', 'штука'),
    ('ст.л.', 'столовая ложка'),
    ('по вкусу', 'по вкусу'),
    ('щепотка', 'щепотка'),
]


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цветовой HEX-код',
        validators=[
            RegexValidator(
                regex=r'^#[0-9A-Fa-f]{6}$',
                message='Цветовой код должен быть в формате #RRGGBB',
                code='invalid_HEX_code'
            )
        ]
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    count = models.IntegerField(
        verbose_name='Количество',
    )
    measurement_unit = models.CharField(
        choices=UNIT_CHOICES,
        verbose_name='Единицы измерения',
        max_length=20,
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(1, message='Введите значение не менее 1')
        ],
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'

    class Meta:
        verbose_name = 'Список покупок'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorite_recipes',
        verbose_name='Пользователь',
    )
    favorite_recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Избранное',
    )

    def __str__(self):
        return f'Рецепт {self.favorite_recipes} в избранном у {self.user}'

    class Meta:
        verbose_name = 'Избранное'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Автор',
    )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        default=1,
        validators=(
            MinValueValidator(1, message='Введите значение не менее 1'),
        ),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'В рецепте {self.recipe.name} {self.amount} '
                f'{self.ingredient.measurement_unit} {self.ingredient.name}')
