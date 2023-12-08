from django_filters import rest_framework as filters

from .choices import CourseChoices, CourseFormatChoices, CourseTypeChoices, StatusChoices


class OrderFilter(filters.FilterSet):
    name_contains = filters.CharFilter('name', 'icontains')
    surname_contains = filters.CharFilter('surname', 'icontains')
    email_contains = filters.CharFilter('email', 'icontains')
    phone_contains = filters.NumberFilter('phone', 'icontains')
    age_in = filters.BaseInFilter('age')
    course = filters.ChoiceFilter('course', choices=CourseChoices.choices)
    course_format = filters.ChoiceFilter('course_format', choices=CourseFormatChoices.choices)
    course_type = filters.ChoiceFilter('course_type', choices=CourseTypeChoices.choices)
    status_in = filters.ChoiceFilter('status', choices=StatusChoices.choices)
    group = filters.CharFilter('group__id', 'icontains')
    created_at = filters.DateFromToRangeFilter()
    manager = filters.CharFilter('manager__name', 'icontains')
    order_by = filters.OrderingFilter(
        fields=(
            'id',
            'name',
            'surname',
            'email',
            'phone',
            'age',
            'course',
            'course_format',
            'course_type',
            'status',
            'sum',
            'already_paid',
            'created_at',
            'updated_at',
            'group',
            'manager',
        )
    )
