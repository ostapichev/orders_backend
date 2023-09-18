from django.db import models


class CourseTypeChoices(models.TextChoices):
    all_types = 'all_types'
    pro = 'pro'
    minimal = 'minimal'
    premium = 'premium'
    incubator = 'incubator'
    vip = 'vip'
    