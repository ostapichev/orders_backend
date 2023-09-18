from django.db import models


class CourseChoices(models.TextChoices):
    all_courses = 'all courses'
    FS = 'FS'
    QACX = 'QASX'
    JCX = 'JSX'
    JSCX = 'JSCX'
    FE = 'FE'
    PCX = 'PCX'
