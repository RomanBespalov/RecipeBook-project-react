# Generated by Django 4.2.3 on 2023-08-19 14:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_remove_ingredient_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribe',
            name='author',
        ),
        migrations.RemoveField(
            model_name='subscribe',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
        migrations.DeleteModel(
            name='Subscribe',
        ),
    ]
