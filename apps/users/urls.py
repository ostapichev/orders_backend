from django.urls import path

from .views import UserListCreate

urlpatterns = [
    path('', UserListCreate.as_view(), name='user_list_create'),
]