from django.contrib import admin

from recipes.models import Tags, Recipe, Ingredients
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name',
    )


class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug',
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'image', 'text',
    )


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'measurement_unit',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
