from django.db import models


class CourseFormatChoices(models.TextChoices):
    static = 'static'
    online = 'online'
    