from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

from core.models import ProfileModel


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_user(self, email, password='admin', **kwargs):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        try:
            if kwargs['is_superuser']:
                profile_data = {"name": "Admin", "surname": "Super"}
                profile = ProfileModel(**profile_data)
                profile.save()
                user.profile = profile
        except KeyError:
            pass
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if not kwargs['is_superuser']:
            raise ValueError('Superuser must be have is_superuser')
        user = self.create_user(email, password, **kwargs)
        return user

    def all_with_profiles(self):
        return self.select_related('profile')
