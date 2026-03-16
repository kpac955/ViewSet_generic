from django.urls import path
from .views import UserUpdateAPIView, UserRetrieveAPIView
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
]