from django.db import models


class StatusChoices(models.TextChoices):
    all_statuses = 'all statuses'
    in_work = 'in work'
    new = 'new'
    agree = 'agree'
    disagree = 'disagree'
    dubbing = 'dubbing'
