from django_filters import rest_framework as filters


class GroupFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=('id',)
    )
