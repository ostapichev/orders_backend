from rest_framework import serializers

from .models import CommentModel, OrderModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('id', 'comment')


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
            'updated_at',
            'comments',
        )



