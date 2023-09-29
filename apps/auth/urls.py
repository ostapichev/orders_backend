from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ActivateUserView, MeView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='access_refresh_token'),
    path('/activate/<str:token>', ActivateUserView.as_view(), name='activate_user'),
    path('/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('/me', MeView.as_view(), name='me')
]
