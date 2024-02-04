from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

import pandas as pd
from drf_yasg.utils import no_body, swagger_auto_schema

from core.services.export_file_service import ExportFileService

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
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        order = self.get_object()
        try:
            if self.request.data['status'] == 'new_order':
                order.manager_id = None
            if self.request.user.id != order.manager_id:
                if order.manager_id:
                    return Response({'detail': "You don't have permissions"}, status.HTTP_403_FORBIDDEN)
        except KeyError:
            return Response({'detail': 'Status is not valid'}, status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class CommentListCreateView(GenericAPIView):
    """
        get:
            Get all comments
        post:
            Create comment under order by id
    """
    serializer_class = CommentSerializer
    queryset = OrderModel.objects.all()
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=no_body)
    def get(self, *args, **kwargs):
        order = self.get_object()
        comments = CommentModel.objects.filter(order=order)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    def post(self, *args, **kwargs):
        order = self.get_object()
        if order.manager_id is not None and self.request.user.id != order.manager_id:
            return Response({'detail': "You don't have permissions"}, status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order, profile_id=self.request.user.profile.id)
        order.manager_id = self.request.user.profile.id
        order.status = StatusChoices.in_work
        order.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


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
        data = list(orders.values())
        ExportFileService.date_converter(data)
        df = pd.DataFrame(data)
        filename = ExportFileService.name_creator()
        excluded_columns = ['msg', 'utm', 'comments']
        data_table = df.drop(columns=excluded_columns, errors='ignore')
        response = ExportFileService.book_creator(data_table, filename)
        return response
