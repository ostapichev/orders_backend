from django.db import models

from core.models import BaseModel


class OrderModel(BaseModel):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.BigIntegerField(unique=True)
    age = models.IntegerField()
    course = models.CharField(max_length=5)
    course_format = models.CharField(max_length=10)
    course_type = models.CharField(max_length=20)
    already_paid = models.IntegerField()
    sum = models.IntegerField()
    msg = models.TextField(max_length=255)
    status = models.CharField(max_length=10)
    utm = models.CharField(max_length=35)

    class Meta:
        db_table = 'orders'


class CommentModel(BaseModel):
    comment = models.TextField()
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
