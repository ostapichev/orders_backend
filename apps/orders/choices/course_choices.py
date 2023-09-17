from django.db import models


class CourseChoices(models.TextChoices):
    FS = 'FS',
    QACX = 'QASX',
    JCX = 'JSX',
    JSCX = 'JSCX',
    FE = 'FE',
    PCX = 'PCX',
