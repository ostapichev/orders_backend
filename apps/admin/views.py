from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permission.is_superuser import IsSuperUser

from apps.orders.choices import StatusChoices
from apps.orders.models import OrderModel
from apps.orders.serializers import OrderSerializer
from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()


class UserCreateView(CreateAPIView):
    """
        Create user
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    permission_classes = (IsSuperUser,)


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
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        item_count = OrderModel.objects.count()
        in_work = OrderModel.objects.filter(status=StatusChoices.in_work).count()
        new_order = OrderModel.objects.filter(status=StatusChoices.new_order).count()
        agree = OrderModel.objects.filter(status=StatusChoices.agree).count()
        disagree = OrderModel.objects.filter(status=StatusChoices.disagree).count()
        dubbing = OrderModel.objects.filter(status=StatusChoices.dubbing).count()
        return Response({
            'item_count': item_count,
            StatusChoices.in_work: in_work,
            StatusChoices.new_order: new_order,
            StatusChoices.agree: agree,
            StatusChoices.disagree: disagree,
            StatusChoices.dubbing: dubbing
        }, status.HTTP_200_OK)


class StatisticUsersView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        count_orders = OrderModel.objects.filter(manager=kwargs['pk']).count()
        in_work = OrderModel.objects.filter(manager=kwargs['pk'], status='in_work').count()
        agree = OrderModel.objects.filter(manager=kwargs['pk'], status='agree').count()
        return Response({
            'count_orders': count_orders,
            'in_work': in_work,
            'agree': agree
        }, status.HTTP_200_OK)
