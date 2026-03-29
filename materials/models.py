from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/", verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id"]


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/", verbose_name="Превью", **NULLABLE)
    video_url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")
