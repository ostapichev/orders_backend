from django.urls import path

from .views import StatisticOrdersView, StatisticUsersView, UserBanView, UserCreateView, UserUnBanView

urlpatterns = [
    path('/users', UserCreateView.as_view(), name='create_user'),
    path('/users/<int:pk>/ban', UserBanView.as_view(), name='user_ban'),
    path('/users/<int:pk>/unban', UserUnBanView.as_view(), name='user_unban'),
    path('/statistic/orders', StatisticOrdersView.as_view(), name='statistic_orders'),
    path('/statistic/users/<int:pk>', StatisticUsersView.as_view(), name='statistic_users'),
]
