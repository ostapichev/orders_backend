from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from core.permission.is_superuser import IsSuperUser
from core.services.jwt_service import ActivateToken, JWTService

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()


class ActivateUserView(GenericAPIView):
    permission_classes = (IsSuperUser,)

    def post(self, *args, **kwargs):
        token = kwargs['token']
        user: User = JWTService.validate_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MeView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
