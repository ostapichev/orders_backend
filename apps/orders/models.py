from django.db import models

from apps.groups.models import GroupModel
from apps.orders.choices import CourseChoices, CourseFormatChoices, CourseTypeChoices, StatusChoices
from core.models import BaseModel, ProfileModel


class OrderModel(BaseModel):
    name = models.CharField(max_length=25, null=True)
    surname = models.CharField(max_length=25, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=12, null=True)
    age = models.IntegerField(null=True)
    course = models.CharField(max_length=10, choices=CourseChoices.choices, null=True)
    course_format = models.CharField(max_length=15, choices=CourseFormatChoices.choices, null=True)
    course_type = models.CharField(max_length=100, choices=CourseTypeChoices.choices, null=True)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, null=True)
    sum = models.IntegerField(null=True)
    alreadyPaid = models.IntegerField(null=True)
    utm = models.CharField(max_length=100, null=True)
    msg = models.CharField(max_length=100, null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT, related_name='orders', null=True)
    manager = models.ForeignKey(ProfileModel, on_delete=models.PROTECT, related_name='order', null=True)

    class Meta:
        db_table = 'orders'
        ordering = ('-id',)


class CommentModel(BaseModel):
    comment = models.TextField()
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
        ordering = ('-id',)
