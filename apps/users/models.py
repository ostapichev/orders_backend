from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from core.models import BaseModel

from .managers import UserManager


class UserModel(AbstractUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserManager()

    class Meta:
        db_table = 'auth.user'
