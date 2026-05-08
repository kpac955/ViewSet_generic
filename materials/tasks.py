from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправка письма подписчикам при обновлении курса"""
    # 1. Получаем курс
    course = Course.objects.get(pk=course_id)

    # 2. Ищем все подписки на этот курс
    subscriptions = Subscription.objects.filter(course=course).select_related("user")
    recipient_list = [sub.user.email for sub in subscriptions]

    # 3. Если есть кому отправлять — отправляем
    if recipient_list:
        send_mail(
            subject=f'Курс "{course.title}" обновлен!',
            message=f'Привет! В курсе "{course.title}" появились новые материалы. Скорее заходи проверить!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
