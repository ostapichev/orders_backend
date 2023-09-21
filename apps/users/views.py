from django.contrib.auth import get_user_model

from rest_framework.generics import ListCreateAPIView

from .models import UserModel as User
from .serializers import UserSerializer

UserModel: User = get_user_model()


class UserListCreate(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
