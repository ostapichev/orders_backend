from django.db import models


class StatusChoices(models.TextChoices):
    in_work = 'in work',
    new = 'new',
    agree = 'agree',
    disagree = 'disagree',
    dubbing = 'dubbing'
