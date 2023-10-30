from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ActivateUserRequestView, ActivateUserView, MeView, RecoveryPasswordRequestView, RecoveryPasswordView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='access_refresh_token'),
    path('/activate', ActivateUserRequestView.as_view(), name='activate_user'),
    path('/activate/<str:token>', ActivateUserView.as_view(), name='activate_request_user'),
    path('/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('/recovery_password', RecoveryPasswordRequestView.as_view(), name='recovery_password_request'),
    path('/recovery_password/<str:token>', RecoveryPasswordView.as_view(), name='recovery_password'),
    path('/me', MeView.as_view(), name='me'),
]
