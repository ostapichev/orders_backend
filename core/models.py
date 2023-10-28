from django.core import validators
from django.db import models

from core.enums import RegExEnum


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProfileModel(BaseModel):
    name = models.CharField(max_length=50, validators=[
        validators.RegexValidator(RegExEnum.BASE_NAME_PATTERN.pattern, RegExEnum.BASE_NAME_PATTERN.msg)
    ])
    surname = models.CharField(max_length=50, validators=[
        validators.RegexValidator(RegExEnum.BASE_NAME_PATTERN.pattern, RegExEnum.BASE_NAME_PATTERN.msg)
    ])

    class Meta:
        db_table = 'profile'
