from collections import OrderedDict
from io import BytesIO

from django.http import FileResponse, Http404, HttpResponse

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

import pandas as pd

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

    def get(self, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=kwargs['pk'])
        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=kwargs['pk'])
        if self.request.user.id != order.manager_id:
            raise Http404()
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

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not OrderModel.objects.filter(pk=pk).exists():
            raise Http404()
        comments = CommentModel.objects.filter(order_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=kwargs['pk'])
        if order.manager_id is not None and self.request.user.id != order.manager_id:
            raise Http404()
        serializer = CommentSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order, profile_id=self.request.user.profile.id)
        order.manager_id = self.request.user.profile.id
        order.status = StatusChoices.in_work
        order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExcelExportAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get(self, *args, **kwargs):
        orders = OrderModel.objects.all()
        serializer = OrderSerializer(orders, many=True)
        data = []
        for item in serializer.data:
            processed_data = {}
            for key, value in item.items():
                if isinstance(value, OrderedDict):
                    selected_keys = ['name']
                    selected_data = ', '.join([f'{value[key]}' for key in selected_keys])
                    processed_data[key] = selected_data
                else:
                    processed_data[key] = value
            data.append(processed_data)
        df = pd.DataFrame(data)
        excluded_columns = ['msg', 'utm', 'comments']
        df = df.drop(columns=excluded_columns, axis=1)
        excel_buffer = BytesIO()
        try:
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            excel_buffer_content = excel_buffer.getvalue()
            response = HttpResponse(
                excel_buffer_content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=orders_data.xlsx'
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            excel_buffer.close()
        return response
