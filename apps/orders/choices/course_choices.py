from django.db import models


class CourseChoices(models.TextChoices):
    FS = 'FS'
    QACX = 'QACX'
    JCX = 'JCX'
    JSCX = 'JSCX'
    FE = 'FE'
    PCX = 'PCX'
