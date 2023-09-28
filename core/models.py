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
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg)
    ])
    surname = models.CharField(max_length=50, validators=[
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg)
    ])

    class Meta:
        db_table = 'profile'

