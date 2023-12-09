from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permission.is_superuser import IsSuperUser

from apps.admin.models import UserModel as User
from apps.admin.serializers import StatisticOrdersSerializer, StatisticUserSerializer, UserSerializer
from apps.orders.choices import StatusChoices
from apps.orders.models import OrderModel

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
        Statistic orders
    """
    serializer_class = StatisticOrdersSerializer
    permission_classes = (IsAdminUser,)
    super_user_count = 1

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
            'user_count': user_count - self.super_user_count,
            'in_work': in_work,
            'new_order': new_order,
            'agree': agree,
            'disagree': disagree,
            'dubbing': dubbing
        }
        serializer = StatisticOrdersSerializer(statistic_orders)
        return Response(serializer.data, status.HTTP_200_OK)


class StatisticUsersView(GenericAPIView):
    """
    Get statistics for multiple users
    """
    serializer_class = StatisticUserSerializer
    permission_classes = (IsSuperUser,)

    def get(self, request, *args, **kwargs):
        user_ids = str(kwargs['pk'])
        if not user_ids:
            return Response({'detail': 'Please provide at least one user_id'}, status=status.HTTP_400_BAD_REQUEST)

        statistics = []
        for user_id in user_ids:
            user = get_object_or_404(UserModel, pk=user_id)
            count_orders = OrderModel.objects.filter(manager=user_id).count()
            in_work = OrderModel.objects.filter(manager=user_id, status='in_work').count()
            agree = OrderModel.objects.filter(manager=user_id, status='agree').count()
            user_statistics = {
                'user_id': user_id,
                'count_orders': count_orders,
                StatusChoices.in_work: in_work,
                StatusChoices.agree: agree
            }
            statistics.append(user_statistics)

        serializer = StatisticUserSerializer(statistics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
