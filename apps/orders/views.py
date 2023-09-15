from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderModel
from .serializers import OrderSerializer


class OrdersListCreateView(APIView):

    def get(self, *args, **kwargs):
        orders = OrderModel.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data: dict = self.request.data
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class OrderRetrieveUpdateDestroyView(APIView):
    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        try:
            order = OrderModel.objects.get(pk=pk)
        except OrderModel.DoesNotExist:
            raise Http404()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        pk = kwargs['pk']
        data: dict = self.request.data
        try:
            order = OrderModel.objects.get(pk=pk)
        except OrderModel.DoesNotExist:
            raise Http404()
        serializer = OrderSerializer(order, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        pk = kwargs['pk']
        try:
            order = OrderModel.objects.get(pk=pk)
            order.delete()
        except OrderModel.DoesNotExist:
            raise Http404()
        return Response('Deleted', status.HTTP_204_NO_CONTENT)
