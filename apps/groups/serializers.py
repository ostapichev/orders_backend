from rest_framework import serializers

from apps.orders.serializers import OrderSerializer

from .models import GroupModel


class GroupSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = GroupModel
        fields = ('id', 'name', 'orders')
