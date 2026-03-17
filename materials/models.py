from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lessons/', verbose_name='Превью', blank=True, null=True)
    video_url = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
