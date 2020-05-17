from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import registration

urlpatterns = [
    path("register/", registration, name="account_register"),
    path("login/", TokenObtainPairView.as_view(), name="account_login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
