from django.db import models

class NameEvents(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'
        ordering = ['name']

    def __str__(self):
        return self.name


class Events(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название события')
    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE, 
        related_name='events', 
        null=True, blank=True, 
        verbose_name='Пользователь')
    
    event_type = models.ForeignKey(NameEvents, on_delete=models.SET_NULL, null=True, blank=True, related_name='event_items', verbose_name='Тип события')

    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    data = models.DateField(verbose_name='Дата')
    reminder_time = models.TimeField(null=True, blank=True, verbose_name='Время напоминания')

    project = models.CharField(max_length=64, verbose_name='Проект', blank=True)
    type = models.CharField(max_length=128, verbose_name='важное или нет')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['-data', 'start_time']

    def __str__(self):
        return f"{self.name} - {self.data} {self.start_time}"
    