from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permission.is_superuser import IsSuperUser

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()


class UserCreateView(CreateAPIView):
    """
        Create user
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    permission_classes = (AllowAny,)


class UserBanView(GenericAPIView):
    """
        Block user by id
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserUnBanView(GenericAPIView):
    """
        Unblock user by id.
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)
