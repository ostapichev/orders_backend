from django.urls import path

from .views import GroupOrderListCreateView, GroupsListCreateView, GroupUpdateDestroyView

urlpatterns = [
    path('', GroupsListCreateView.as_view(), name='list_create_group'),
    path('/<int:pk>', GroupUpdateDestroyView().as_view(), name='retrieve_update_destroy_group'),
    path('/<int:pk>/orders', GroupOrderListCreateView.as_view(), name='create_list_create_order'),
]
