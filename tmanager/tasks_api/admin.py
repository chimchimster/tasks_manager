from django.contrib import admin

from .models import *


@admin.register(Task)
class AdminTask(admin.ModelAdmin):

    list_display = ['title', 'description', 'status', 'priority', 'get_tags', 'created_at', 'due_to']
    list_filter = ['status', 'priority', 'created_at', 'due_to']
    list_editable = ['status', 'priority', 'due_to']

    def get_tags(self, obj):
        return ", ".join([str(tag) for tag in obj.tags.all()])


@admin.register(Board)
class AdminBoard(admin.ModelAdmin):

    list_display = ['title', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']


@admin.register(TaskHistory)
class AdminTaskHistory(admin.ModelAdmin):

    list_display = ['task', 'user', 'timestamp', 'previous_status', 'current_status']


admin.site.register(Status)
admin.site.register(Tag)
admin.site.register(Priority)
