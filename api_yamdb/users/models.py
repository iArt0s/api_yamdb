from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE = [
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
        ('admin', 'Админ')
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    confirmation_code = models.CharField(
        max_length=300, unique=True, blank=False, null=True)
    is_active = models.BooleanField(
        default=True,
    )
    role = models.CharField(max_length=20, choices=ROLE, default='user')

    bio = models.TextField(
        'Биография',
        blank=False,
        null=True
    )
