from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.orders.models import OrderModel

from apps.admin.managers import UserManager
from core.models import BaseModel, ProfileModel


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='user')
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        ordering = ('-id',)
