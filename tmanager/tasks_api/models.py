from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


class Board(models.Model):

    title = models.CharField(max_length=50, verbose_name='Заголовок борда', blank=False, null=False)
    description = models.TextField(verbose_name='Описание борда', blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Время создания борда')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Время изменения борда')

    def can_be_destroyed(self, user):
        if user.is_staff():
            return True
        return False

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Борд'
        verbose_name_plural = 'Борды'


class Status(models.Model):

    STATUSES = (
        ('to_do', 'В ожидании начала исполнения'),
        ('in_progress', 'В процессе исполнения'),
        ('done', 'Завершено')
    )

    status = models.CharField(max_length=15, choices=STATUSES, verbose_name='Статус задачи')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Tag(models.Model):

    TAGS = (
        ('backend', 'Бэкенд'),
        ('frontend', 'Фронтенд'),
        ('testing', 'Тестирование'),
        ('deploy', 'Деплой'),
    )

    tags = models.CharField(max_length=15, choices=TAGS, verbose_name='Метка задачи')

    def __str__(self):
        return self.tags

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'


class Priority(models.Model):

    PRIORITIES = (
        ('urgently', 'Срочно'),
        ('ordinary', 'Нормально'),
    )

    priorities = models.CharField(max_length=15, choices=PRIORITIES, verbose_name='Приоритет задачи')

    def __str__(self):
        return self.priorities

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'


class Task(models.Model):

    board_id = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='cards', verbose_name='Борд')
    participants = models.ManyToManyField(User, verbose_name='Участники')
    title = models.CharField(max_length=50, verbose_name='Заголовок задачи', blank=False, null=False)
    description = models.TextField(verbose_name='Описание задачи', blank=False, null=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус задачи')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, verbose_name='Приоритет задачи')
    tags = models.ManyToManyField(Tag, verbose_name='Метки')
    attachment = models.FileField(upload_to='media/%d/%m/%Y', blank=True, null=True)
    created_at = models.DateField(auto_now=True, verbose_name='Время создания задачи')
    due_to = models.DateField(verbose_name='Дедлайн', blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [F('board_id__updated_at').desc()]
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

        # Индексация полей status и due_to имеет смысл поскольку
        # запросы на фильтрацию по дате и статусу входят в ТЗ.
        # Однако, важно помнить, что при изменении или удалении
        # записей индексы будут пересчитываться. При высокой нагрузке
        # это может сказываться на производительности.
        indexes = [
            models.Index(fields=['board_id']),
            models.Index(fields=['status']),
            models.Index(fields=['due_to']),
            models.Index(fields=['title']),
        ]


class TaskHistory(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history', verbose_name='Задача')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время изменения')
    description = models.TextField(verbose_name='Описание изменения')

    class Meta:
        verbose_name = 'История задачи'
        verbose_name_plural = 'История задач'

    def __str__(self):
        return '%s - %s' % (self.task, self.timestamp)


__all__ = [
    'Board',
    'Status',
    'Tag',
    'Priority',
    'Task',
    'TaskHistory',
]
