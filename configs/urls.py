from django.urls import include, path

urlpatterns = [
    path('orders', include('apps.orders.urls')),
    path('groups', include('apps.groups.urls')),
]
