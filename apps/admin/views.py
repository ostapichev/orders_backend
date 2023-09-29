from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from core.permission.is_superuser import IsSuperUser
from core.services.email_service import EmailService

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    permission_classes = (IsSuperUser,)


class UserBanView(GenericAPIView):
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()

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
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class TestEmail(GenericAPIView):
    permission_classes = (IsSuperUser,)

    def get(self, *args, **kwargs):
        EmailService.test_email()
        return Response('ok')
