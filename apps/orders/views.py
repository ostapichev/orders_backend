from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .filters import order_filtered_queryset
from .models import OrderModel
from .serializers import OrderSerializer


class OrdersListCreateView(GenericAPIView):
    def get(self, *args, **kwargs):
        qs = order_filtered_queryset(self.request.query_params)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data: dict = self.request.data
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class OrderRetrieveUpdateDestroyView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()

    def get(self, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        data: dict = self.request.data
        order = self.get_object()
        serializer = OrderSerializer(order, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.get_object().delete()
        return Response('Deleted', status.HTTP_204_NO_CONTENT)
