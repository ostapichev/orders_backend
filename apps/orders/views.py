from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderModel


class OrdersListCreateView(APIView):
    def post(self, *args, **kwargs):
        return Response('Method POST')

    def get(self, *args, **kwargs):
        return Response('Method GET')


class OrderView(APIView):
    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        return Response(f'Method GET, order id: {pk}')

    def patch(self, *args, **kwargs):
        pk = kwargs['pk']
        return Response(f'Method PATCH, order id: {pk}')
