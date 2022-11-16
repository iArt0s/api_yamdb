from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    confirmation_code = models.CharField(
        max_length=300, unique=True, blank=False, null=True)
    is_active = models.BooleanField(
        default=False,
    )
    role = models.ManyToManyField('user', 'admin', 'moderator')
    
