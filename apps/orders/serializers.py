from rest_framework import serializers

from .models import OrderModel


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=35)
    surname = serializers.CharField(max_length=35)
    email = serializers.EmailField(max_length=254)
    phone = serializers.IntegerField()
    age = serializers.IntegerField()
    course = serializers.CharField(max_length=5)
    course_format = serializers.CharField(max_length=10)
    course_type = serializers.CharField(max_length=20)
    alreadyPaid = serializers.IntegerField()
    sum = serializers.IntegerField()
    msg = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=10)
    utm = serializers.CharField(max_length=35)

    def create(self, validated_data):
        return OrderModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
