from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


class CanBeDestroyedMixin(models.Model):
    class Meta:
        abstract = True

    def can_be_destroyed(self, user):
        return user.is_staff


class Board(CanBeDestroyedMixin):
    title = models.CharField(max_length=50, verbose_name='Заголовок борда', blank=False, null=False)
    description = models.TextField(verbose_name='Описание борда', blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Время создания борда')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Время изменения борда')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Борд'
        verbose_name_plural = 'Борды'


class Status(CanBeDestroyedMixin):

    STATUSES = (
        ('to_do', 'В ожидании начала исполнения'),
        ('in_progress', 'В процессе исполнения'),
        ('done', 'Завершено')
    )

    status = models.CharField(max_length=15, choices=STATUSES, verbose_name='Статус задачи')

    def __str__(self):
        return self.status

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='status_unique',
                fields=['status'],
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Tag(CanBeDestroyedMixin):

    TAGS = (
        ('backend', 'Бэкенд'),
        ('frontend', 'Фронтенд'),
        ('testing', 'Тестирование'),
        ('deploy', 'Деплой'),
    )

    tag = models.CharField(max_length=15, choices=TAGS, verbose_name='Метка задачи')

    def __str__(self):
        return self.tag

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='tag_unique',
                fields=['tag'],
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'


class Priority(CanBeDestroyedMixin):

    PRIORITIES = (
        ('urgently', 'Срочно'),
        ('ordinary', 'Нормально'),
    )

    priority = models.CharField(max_length=15, choices=PRIORITIES, verbose_name='Приоритет задачи')

    def __str__(self):
        return self.priority

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='priority_unique',
                fields=['priority'],
                deferrable=models.Deferrable.IMMEDIATE,
            )
        ]
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'


class Task(CanBeDestroyedMixin):

    board_id = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks', verbose_name='Борд')
    participants = models.ManyToManyField(User, verbose_name='Участники')
    title = models.CharField(max_length=50, verbose_name='Заголовок задачи', blank=False, null=False)
    description = models.TextField(blank=False, null=False, verbose_name='Описание задачи')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, blank=True, verbose_name='Приоритет задачи')
    tags = models.ManyToManyField(Tag, blank=False, verbose_name='Метки')
    attachment = models.FileField(upload_to='media/%d/%m/%Y', blank=True, null=True)
    created_at = models.DateField(auto_now=True, verbose_name='Время создания задачи')
    due_to = models.DateField(verbose_name='Дедлайн', blank=False, null=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=False, verbose_name='Статус задачи')

    previous_status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Предыдущий статус'
    )

    def save(self, *args, **kwargs):
        if self.pk:
            obj = Task.objects.get(pk=self.pk)
            if obj.status != self.status:
                self.previous_status = obj.status
        super().save(*args, **kwargs)

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


class TaskHistory(CanBeDestroyedMixin):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history', verbose_name='Задача')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время изменения')
    previous_status = models.CharField(max_length=15, default='to_do', verbose_name='Предыдущий статус')
    current_status = models.CharField(max_length=15, verbose_name='Текущий статус')

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
