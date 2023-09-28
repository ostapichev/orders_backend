from django.urls import include, path

urlpatterns = [
    path('auth', include('apps.auth.urls')),
    path('orders', include('apps.orders.urls')),
    path('groups', include('apps.groups.urls')),
    path('users', include('apps.users.urls')),
    path('admin', include('apps.admin.urls')),
]
