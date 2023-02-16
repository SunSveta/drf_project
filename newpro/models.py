from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):

    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):

    title = models.CharField(max_length=150, verbose_name='Название урока')
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание урока')
    video_link = models.URLField(verbose_name='ссылка на видео')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.title
