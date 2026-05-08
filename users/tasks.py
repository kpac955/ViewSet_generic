from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def block_inactive_users():
    """Блокировка за 30 дней внеактива"""
    limit = timezone.now() - timedelta(days=30)
    # Находим тех, кто не заходил больше месяца
    inactive_users = User.objects.filter(last_login__lt=limit, is_active=True).exclude(
        is_superuser=True
    )
    inactive_users.update(is_active=False)
