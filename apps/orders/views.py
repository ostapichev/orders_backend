from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from .filters import OrderFilter
from .models import CommentModel, OrderModel
from .serializers import CommentSerializer, OrderSerializer


class OrdersListView(GenericAPIView, ListModelMixin):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.prefetch_related('comments')
    filterset_class = OrderFilter

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()


class CommentListCreateView(GenericAPIView):
    queryset = OrderModel.objects.all()

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not OrderModel.objects.filter(pk=pk).exists():
            raise Http404()
        comments = CommentModel.objects.filter(order_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pk = kwargs['pk']
        serializer = CommentSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        if not OrderModel.objects.filter(pk=pk).exists():
            raise Http404()
        serializer.save(order_id=pk)
        return Response(serializer.data, status.HTTP_201_CREATED)
