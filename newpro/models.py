from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):

    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='автор курса', on_delete=models.CASCADE,
                                    **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):

    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса', **NULLABLE)
    title = models.CharField(max_length=150, verbose_name='Название урока')
    preview = models.ImageField(upload_to='lesson/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание урока')
    video_link = models.URLField(verbose_name='ссылка на видео')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор урока', on_delete=models.CASCADE,
                                     **NULLABLE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.title} ({self.course_name})'


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'
    PAY = (
        ('cash', 'наличные'),
        ('transfer', 'перевод на счет')
    )

    paying_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    pay_date = models.TimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course,on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    summ = models.PositiveIntegerField(default=0, verbose_name='Сумма')
    pay_type = models.CharField(max_length=20, choices=PAY, default='transfer', verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.paying_user} - {self.summ}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Subscription(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUSES = (
        ('active', 'подписаны'),
        ('inactive', 'не подписаны')
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE,
                                **NULLABLE)
    course_id = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE, **NULLABLE)
    status = models.CharField(max_length=15, choices=STATUSES, verbose_name='статус подписки', default=INACTIVE)

    def __str__(self):
        return f'{self.course_id}: {self.status}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
