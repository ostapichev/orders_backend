from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from core.services.email_service import EmailService

from .models import ProfileModel
from .models import UserModel as User

UserModel: User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    @transaction.atomic
    def create(self, validated_data: dict):
        profile_data = validated_data.pop('profile')
        profile = ProfileModel.objects.create(**profile_data)
        user = UserModel.objects.create_user(profile=profile, **validated_data)
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'is_active', 'last_login', 'profile')
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
