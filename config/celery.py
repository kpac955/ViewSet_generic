import os

from celery import Celery

# Настройки Django для celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Читаем конфиг из settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматический поиск задач в файлах tasks.py приложений
app.autodiscover_tasks()
