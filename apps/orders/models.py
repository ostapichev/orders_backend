from django.core import validators
from django.db import models

from core.enums import RegExEnum
from core.models import BaseModel

from apps.orders.choices import CourseChoices, CourseFormatChoices, CourseTypeChoices, StatusChoices


class OrderModel(BaseModel):
    name = models.CharField(max_length=35, validators=[
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg)
    ])
    surname = models.CharField(max_length=35, validators=[
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg)
    ])
    email = models.EmailField(max_length=254, unique=True)
    phone = models.BigIntegerField(unique=True, validators=[
        validators.RegexValidator(RegExEnum.PHONE.pattern, RegExEnum.PHONE.msg)
    ])
    age = models.IntegerField(validators=[
        validators.MinValueValidator(10),
        validators.MaxValueValidator(70)
    ])
    course = models.CharField(max_length=4, choices=CourseChoices.choices)
    course_format = models.CharField(max_length=6, choices=CourseFormatChoices.choices)
    course_type = models.CharField(max_length=9, choices=CourseTypeChoices.choices)
    already_paid = models.IntegerField()
    sum = models.IntegerField()
    msg = models.TextField(max_length=255)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    utm = models.CharField(max_length=35)

    class Meta:
        db_table = 'orders'
        ordering = ('id',)


class CommentModel(BaseModel):
    comment = models.TextField()
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
