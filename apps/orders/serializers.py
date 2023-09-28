from rest_framework import serializers

from .models import CommentModel, OrderModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('id', 'comment', 'created_at', 'profile_id')


class OrderSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

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
            'comments',
            'group_id',
            'manager_id',
        )
