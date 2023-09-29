from django.contrib.auth import get_user_model

from rest_framework.generics import ListAPIView

from core.permission.is_superuser import IsSuperUser

from .models import UserModel as User
from .serializers import UserSerializer

UserModel: User = get_user_model()


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    permission_classes = (IsSuperUser,)

    def get_permissions(self):
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)
