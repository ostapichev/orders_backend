from django.contrib.auth import get_user_model

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from core.permission.is_superuser import IsSuperUser

from .filters import UserFilter
from .models import UserModel as User
from .serializers import UserSerializer

UserModel: User = get_user_model()


class UserListView(ListAPIView):
    """
        Get all users
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    permission_classes = (AllowAny,)
    filterset_class = UserFilter

    def get_permissions(self):
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)
