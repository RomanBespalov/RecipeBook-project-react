# Generated by Django 3.2 on 2023-08-24 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_subscribe_user_unique_user_subscribe_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Subscribe',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
