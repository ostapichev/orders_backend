from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.models import BaseModel

from .managers import UserManager


class ProfileModel(BaseModel):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    class Meta:
        db_table = 'profile'


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='user')
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)



