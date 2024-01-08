from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    name_contains = filters.CharFilter('profile__name', 'icontains')
    surname_contains = filters.CharFilter('profile__surname', 'icontains')
    email_contains = filters.CharFilter('email', 'icontains')
