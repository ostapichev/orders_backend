from django.db import models


class CourseTypeChoices(models.TextChoices):
    pro = 'pro',
    minimal = 'minimal',
    premium = 'premium',
    incubator = 'incubator',
    vip = 'vip'
    