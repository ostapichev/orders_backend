from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

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
        fields = ('id', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'profile')
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class StatisticOrdersSerializer(serializers.Serializer):
    item_count = serializers.IntegerField()
    user_count = serializers.SerializerMethodField()
    in_work = serializers.IntegerField()
    new_order = serializers.IntegerField()
    agree = serializers.IntegerField()
    disagree = serializers.IntegerField()
    dubbing = serializers.IntegerField()

    def get_user_count(self, obj):
        return obj['user_count']

    class Meta:
        fields = ('item_count', 'user_count', 'in_work', 'new_order', 'agree', 'disagree', 'dubbing')



