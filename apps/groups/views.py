from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from ..orders.models import OrderModel
from ..orders.serializers import OrderSerializer
from .models import GroupModel
from .serializers import GroupSerializer


class GroupsListCreateView(GenericAPIView, CreateModelMixin, ListModelMixin):
    serializer_class = GroupSerializer
    queryset = GroupModel.objects.all()

    def get(self, request,  *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class GroupOrderListCreateView(GenericAPIView):
    queryset = GroupModel.objects.all()

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not GroupModel.objects.filter(pk=pk).exists():
            raise Http404
        orders = OrderModel.objects.filter(group_id=pk)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pk = kwargs['pk']
        serializer = OrderSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        if not GroupModel.objects.filter(pk=pk).exists():
            raise Http404()
        serializer.save(group_id=pk)
        return Response(serializer.data, status.HTTP_201_CREATED)
