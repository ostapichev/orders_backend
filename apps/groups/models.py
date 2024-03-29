from django.core import validators
from django.db import models

from core.enums import RegExEnum
from core.models import BaseModel

from .managers import GroupManager


class GroupModel(BaseModel):
    name = models.CharField(max_length=35, unique=True, validators=[
        validators.RegexValidator(RegExEnum.GROUP.pattern, RegExEnum.GROUP.msg)
    ])
    objects = GroupManager()

    class Meta:
        db_table = 'groups'
        ordering = ('-id',)
