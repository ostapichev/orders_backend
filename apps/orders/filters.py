from django.db.models import QuerySet
from django.http import QueryDict

from rest_framework.exceptions import ValidationError

from .models import OrderModel


def order_filtered_queryset(query: QueryDict) -> QuerySet:
    qs = OrderModel.objects.all()
    for k, v in query.items():
        match k:
            case 'order_by_id':
                qs = qs.order_by('-id')
            case 'order_by_id_desc':
                qs = qs.order_by('id')
            case 'course':
                qs = qs.filter(course__exact=v)
            case 'course_format':
                qs = qs.filter(course_format__exact=v)
            case 'course_type':
                qs = qs.filter(course_type__exact=v)
            case 'status':
                qs = qs.filter(status__exact=v)
            case 'name':
                qs = qs.filter(name__icontains=v)
            case 'surname':
                qs = qs.filter(surname__icontains=v)
            case 'age':
                qs = qs.filter(age__exact=v)
            case _:
                raise ValidationError({'default': f'"{k}" not allowed here'})
    return qs
