from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    # Регистрация и авторизация
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),
    # Пользователи
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-get"),
    # Платежи
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-get"),
]
