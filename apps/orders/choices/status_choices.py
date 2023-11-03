from django.db import models


class StatusChoices(models.TextChoices):
    in_work = 'in_work'
    new_order = 'new_order'
    agree = 'agree'
    disagree = 'disagree'
    dubbing = 'dubbing'
