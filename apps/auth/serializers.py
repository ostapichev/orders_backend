from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.admin.models import UserModel as User

UserModel: User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ActivateTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('password',)
