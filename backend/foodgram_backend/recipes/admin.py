from django.contrib import admin

from recipes.models import (
    Tag, Recipe, Ingredient, RecipeIngredient,
    Favorite, ShoppingCart
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    verbose_name = 'Ингредиент для рецепта'
    verbose_name_plural = 'Ингредиенты для рецепта'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )

    def get_tags_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags_display.short_description = 'Теги'

    def get_ingredients_display(self, obj):
        return ", ".join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )
    get_ingredients_display.short_description = 'Ингредиенты'

    def get_favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    get_favorite_count.short_description = 'Добавлений в избранное'

    list_display = ('name', 'text', 'cooking_time', 'author',
                    'pub_date', 'get_ingredients_display',
                    'get_tags_display', 'image', 'get_favorite_count')
    list_filter = ('name', 'author', 'tags')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
