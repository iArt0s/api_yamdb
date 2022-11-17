from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE = [
        ('M', 'Модератор'),
        ('U', 'Пользователь'),
        ('A', 'Админ')
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    confirmation_code = models.CharField(
        max_length=300, unique=True, blank=False, null=True)
    is_active = models.BooleanField(
        default=False,
    )
    role = models.CharField(max_length=1, choices=ROLE, default='U')

    bio = models.TextField(
        'Биография',
        blank=False,
        null=True
    )
