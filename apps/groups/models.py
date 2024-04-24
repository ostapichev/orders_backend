from django.core import validators
from django.db import models

from core.enums import RegExEnum
from core.models import BaseModel


class GroupModel(BaseModel):
    name = models.CharField(max_length=35, null=True, validators=[
        validators.RegexValidator(RegExEnum.GROUP.pattern, RegExEnum.GROUP.msg)
    ])

    class Meta:
        db_table = 'groups'
        ordering = ('-id',)
