from django.urls import path

from .views import GroupOrderListCreateView, GroupsListCreateView

urlpatterns = [
    path('', GroupsListCreateView.as_view(), name='list_create_group'),
    path('/<int:pk>/order', GroupOrderListCreateView.as_view(), name='create_list_create_order'),
]
