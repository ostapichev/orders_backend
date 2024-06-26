from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.exception.order_permission_exception import OrderPermissionException
from core.services.export_file_service import ExportFileService
from core.services.order_service import OrderService

from .choices import StatusChoices
from .filters import OrderFilter
from .models import CommentModel, OrderModel
from .serializers import CommentSerializer, OrderSerializer


class OrdersListView(GenericAPIView, ListModelMixin):
    """
        Get all orders
    """
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.prefetch_related('comments')
    permission_classes = (IsAdminUser,)
    filterset_class = OrderFilter

    @swagger_auto_schema(request_body=no_body)
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderRetrieveUpdateView(GenericAPIView):
    """
        get:
            Get order by id
        patch:
            Partial update order by id
    """
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=no_body)
    def get(self, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=kwargs['pk'])
        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=kwargs['pk'])
        OrderService.patch_method(self.request, order)
        serializer = OrderSerializer(order, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class CommentListCreateView(GenericAPIView, ListModelMixin):
    """
        get:
            Get all comments
        post:
            Create comment under order by id
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        get_object_or_404(OrderModel, pk=order_id)
        return CommentModel.objects.filter(order_id=order_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=kwargs['pk'])
        if order.manager_id and self.request.user.id != order.manager_id:
            raise OrderPermissionException
        serializer = CommentSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order, profile_id=self.request.user.profile.id)
        order.manager_id = self.request.user.profile.id
        order.status = StatusChoices.in_work
        order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExcelExportAPIView(GenericAPIView):
    """
        Get Excel file by orders
    """
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    queryset = OrderModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        params = self.request.query_params
        queryset = OrderFilter(params, queryset=self.queryset).qs
        return queryset.select_related('related_model')

    @swagger_auto_schema(request_body=no_body)
    def get(self, *args, **kwargs):
        orders = self.filter_queryset(self.get_queryset())
        df = ExportFileService.table_creator(orders)
        filename = ExportFileService.name_creator()
        excluded_columns = ('msg', 'utm', 'comments')
        data_table = df.drop(columns=excluded_columns, errors='ignore')
        return ExportFileService.book_creator(data_table, filename)
