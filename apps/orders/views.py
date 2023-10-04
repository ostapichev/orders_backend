from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

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
