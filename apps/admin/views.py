from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permission.is_superuser import IsSuperUser

from apps.admin.filters import UserFilter
from apps.admin.models import UserModel as User
from apps.admin.serializers import UserSerializer
from apps.orders.choices import StatusChoices
from apps.orders.models import OrderModel
from apps.orders.serializers import OrderSerializer

UserModel: User = get_user_model()


class UserListCreateView(ListCreateAPIView):
    """
        get:
            Get all users
        post:
            Create new user
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    permission_classes = (IsSuperUser,)
    filterset_class = UserFilter
    
    def get_permissions(self):
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserBanView(GenericAPIView):
    """
        Block user by id
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

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
    permission_classes = (IsSuperUser,)

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


class StatisticOrdersView(GenericAPIView):
    """
        Get statistic orders
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        item_count = OrderModel.objects.count()
        user_count = UserModel.objects.count()
        in_work = OrderModel.objects.filter(status=StatusChoices.in_work).count()
        new_order = OrderModel.objects.filter(status=StatusChoices.new_order).count()
        agree = OrderModel.objects.filter(status=StatusChoices.agree).count()
        disagree = OrderModel.objects.filter(status=StatusChoices.disagree).count()
        dubbing = OrderModel.objects.filter(status=StatusChoices.dubbing).count()
        statistic_orders = {
            'item_count': item_count,
            'user_count': user_count,
            StatusChoices.in_work: in_work,
            StatusChoices.new_order: new_order,
            StatusChoices.agree: agree,
            StatusChoices.disagree: disagree,
            StatusChoices.dubbing: dubbing
        }
        return Response(statistic_orders, status.HTTP_200_OK)


class StatisticUsersView(GenericAPIView):
    """
        Get statistic users
    """
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        get_object_or_404(UserModel, pk=user_id)
        count_orders = OrderModel.objects.filter(manager=user_id).count()
        in_work = OrderModel.objects.filter(manager=kwargs['pk'], status='in_work').count()
        agree = OrderModel.objects.filter(manager=kwargs['pk'], status='agree').count()
        statistic_user = {
            'count_orders': count_orders,
            StatusChoices.in_work: in_work,
            StatusChoices.agree: agree
        }
        return Response(statistic_user, status.HTTP_200_OK)
