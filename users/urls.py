from django.urls import path

from .apps import UsersConfig
from .views import UserUpdateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
]
