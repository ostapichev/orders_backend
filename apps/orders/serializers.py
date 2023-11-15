from rest_framework import serializers

from ..admin.serializers import ProfileSerializer
from .models import CommentModel, OrderModel


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CommentModel
        fields = ('id', 'comment', 'created_at', 'profile')


class OrderSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    manager = ProfileSerializer(read_only=True)

    class Meta:
        model = OrderModel
        fields = (
            'id',
            'name',
            'surname',
            'email',
            'phone',
            'age',
            'course',
            'course_format',
            'course_type',
            'status',
            'sum',
            'already_paid',
            'created_at',
            'group',
            'manager',
            'msg',
            'utm',
            'comments',
        )
