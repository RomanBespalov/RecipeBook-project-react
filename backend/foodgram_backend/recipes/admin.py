from django.contrib import admin

from recipes.models import Tag, Recipe, Ingredient
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug',
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'image', 'text',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'measurement_unit',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
