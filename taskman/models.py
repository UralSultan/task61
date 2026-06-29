from django.contrib.auth.models import User
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'

    def __str__(self):
        return self.name


class Project(models.Model):
    start_date = models.DateField(null=False, blank=False, verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')
    description = models.TextField(null=False, blank=False, verbose_name='Описание')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-start_date']

    def __str__(self):
        return self.title



class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True, verbose_name='Проект')
    summary = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT, related_name='tasks',)
    type = models.ManyToManyField('TaskType', related_name='tasks', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks',null=True, verbose_name='Автор')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created']

    def __str__(self):
        return self.summary
