# Generated by Django 3.2 on 2023-09-27 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0031_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=1, upload_to='recipes/images/', verbose_name='Картинка'),
            preserve_default=False,
        ),
    ]
