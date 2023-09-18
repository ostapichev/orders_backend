from django.urls import path

from .views import CommentListCreateView, CommentUpdateDestroyView, OrderRetrieveUpdateDestroyView, OrdersListView

urlpatterns = [
    path('', OrdersListView.as_view(), name='list_create_orders'),
    path('/<int:pk>', OrderRetrieveUpdateDestroyView.as_view(), name='retrieve_update_destroy_order'),
    path('/<int:pk>/comments', CommentListCreateView.as_view(), name='orders_create_comment'),
    path('/comment/<int:pk>', CommentUpdateDestroyView.as_view(), name='orders_create_comment'),
]