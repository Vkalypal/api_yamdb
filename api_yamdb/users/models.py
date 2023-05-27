from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    # INFO: переопределены только те поля, к которым особые требования
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=9,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
