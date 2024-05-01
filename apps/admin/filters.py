from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    name = filters.CharFilter('profile__name', 'icontains')
    surname = filters.CharFilter('profile__surname', 'icontains')
    email = filters.CharFilter('email', 'icontains')
