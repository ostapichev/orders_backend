from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=('id',)
    )
