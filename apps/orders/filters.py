from django_filters import rest_framework as filters

from .choices import CourseChoices, CourseFormatChoices, CourseTypeChoices, StatusChoices


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter('name', 'icontains')
    surname = filters.CharFilter('surname', 'icontains')
    email = filters.CharFilter('email', 'icontains')
    phone = filters.NumberFilter('phone', 'icontains')
    age = filters.BaseInFilter('age')
    course = filters.ChoiceFilter('course', choices=CourseChoices.choices)
    course_format = filters.ChoiceFilter('course_format', choices=CourseFormatChoices.choices)
    course_type = filters.ChoiceFilter('course_type', choices=CourseTypeChoices.choices)
    status = filters.ChoiceFilter('status', choices=StatusChoices.choices)
    group = filters.BaseInFilter('group__id')
    created_at = filters.DateFromToRangeFilter()
    manager = filters.CharFilter('manager__name', 'icontains')
    order_by = filters.OrderingFilter(
        fields=(
            'id', 'name', 'surname', 'email', 'phone', 'age', 'course', 'course_format', 'course_type',
            'status', 'sum', 'already_paid', 'created_at', 'updated_at', 'group', 'manager')
    )
