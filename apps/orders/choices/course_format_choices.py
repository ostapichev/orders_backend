from django.db import models


class CourseFormatChoices(models.TextChoices):
    all_formats = 'all formats'
    static = 'static'
    online = 'online'
    