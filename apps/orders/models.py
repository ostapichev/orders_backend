from django.core import validators
from django.db import models

from core.enums import RegExEnum
from core.models import BaseModel, ProfileModel

from apps.groups.models import GroupModel
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
        validators.MinValueValidator(16),
        validators.MaxValueValidator(90)
    ])
    course = models.CharField(
        max_length=11, choices=CourseChoices.choices, default=CourseChoices.all_courses)
    course_format = models.CharField(
        max_length=11, choices=CourseFormatChoices.choices, default=CourseFormatChoices.all_formats)
    course_type = models.CharField(
        max_length=9, choices=CourseTypeChoices.choices, default=CourseTypeChoices.all_types)
    already_paid = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(2147483647)
        ])
    sum = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(2147483647)
        ])
    utm = models.CharField(max_length=20, null=True)
    msg = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=12, choices=StatusChoices.choices, default=StatusChoices.new)
    group = models.ForeignKey(GroupModel, on_delete=models.PROTECT, related_name='orders', default='all_groups')
    manager = models.ForeignKey(ProfileModel, on_delete=models.PROTECT, related_name='order', null=True)

    class Meta:
        db_table = 'orders'
        ordering = ('id',)


class CommentModel(BaseModel):
    comment = models.TextField()
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
