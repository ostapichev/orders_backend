from django.urls import path

from .views import UserBanView, UserCreateView, UserUnBanView

urlpatterns = [
    path('/users', UserCreateView.as_view(), name='create_user'),
    path('/users/<int:pk>/ban', UserBanView.as_view(), name='user_ban'),
    path('/users/<int:pk>/unban', UserUnBanView.as_view(), name='user_unban'),
]
