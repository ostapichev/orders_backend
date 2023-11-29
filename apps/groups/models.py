from django.core import validators
from django.db import models

from core.enums import RegExEnum
from core.models import BaseModel

from .managers import GroupManager


class GroupModel(BaseModel):
    name = models.CharField(max_length=35, validators=[
        validators.RegexValidator(RegExEnum.GROUP.pattern, RegExEnum.BASE_NAME_PATTERN.msg)
    ])
    objects = GroupManager()

    class Meta:
        db_table = 'groups'
        ordering = ('-id',)
