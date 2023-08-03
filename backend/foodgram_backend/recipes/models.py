from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

UNIT_CHOICES = [
        'г',
        'кг',
        'мл',
        'л',
        'шт',
        'ст.л.',
        'по вкусу',
        'щепотка',
]


class Tags(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='цветовой HEX-код',
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
        verbose_name='идентификатор',
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='название ингредиента',
    )
    count = models.IntegerField(
        verbose_name='количество',
    )
    measurement_unit = models.CharField(
        choices=UNIT_CHOICES,
        verbose_name='единицы измерения',
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='описание',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='теги',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1, message='Введите значение не менее 1')],
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'