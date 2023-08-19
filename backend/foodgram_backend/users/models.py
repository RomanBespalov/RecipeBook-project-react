from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Пользователь',
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]

    def clean(self):
        if self.username == 'me':
            raise ValidationError(
                {'error': 'Невозможно создать пользователя с именем "me".'}
            )

    def __str__(self):
        return self.username


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

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='unique_follower'
            )
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                {'error': 'Невозможно подписаться на себя.'}
            )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
