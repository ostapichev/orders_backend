from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.permission.is_superuser import IsSuperUser
from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.admin.models import UserModel as User
from apps.admin.serializers import UserSerializer

from .serializers import EmailSerializer, PasswordSerializer

UserModel: User = get_user_model()


class ActivateUserRequestView(GenericAPIView):
    """
        Activation user by email
    """
    permission_classes = (IsSuperUser,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        email = data.get('email')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        try:
            EmailService.register_email(user)
        except OSError:
            return Response({'detail': 'Connection locked!'}, status.HTTP_423_LOCKED)
        return Response(f'An email has been sent to {email} for user activation.', status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class ActivateUserView(GenericAPIView):
    """
        Registration user by token
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        token = kwargs['token']
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user: User = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        user.set_password(serializer.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RecoveryPasswordRequestView(GenericAPIView):
    """
        Recovery password by email
    """
    permission_classes = (IsSuperUser,)
    serializer_class = EmailSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        email = data.get('email')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, **serializer.data)
        try:
            EmailService.recovery_email(user)
        except OSError:
            return Response({'detail': 'Connection locked!'}, status.HTTP_423_LOCKED)
        return Response(f'An email has been sent to {email} for password recovery.', status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class RecoveryPasswordView(GenericAPIView):
    """
        New password by token
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer

    def post(self, *args, **kwargs):
        token = kwargs['token']
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user: User = JWTService.validate_token(token, RecoveryToken)
        user.set_password(serializer.data['password'])
        user.save()
        return Response('Password changed', status.HTTP_200_OK)


class MeView(RetrieveAPIView):
    """
        Get me data
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
