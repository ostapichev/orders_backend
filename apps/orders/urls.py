from django.urls import path

from .views import CommentListCreateView, OrderRetrieveUpdateView, OrdersListView

urlpatterns = [
    path('', OrdersListView.as_view(), name='list_create_orders'),
    path('/<int:pk>', OrderRetrieveUpdateView.as_view(), name='retrieve_update_destroy_order'),
    path('/<int:pk>/comments', CommentListCreateView.as_view(), name='orders_create_comment'),
]
