from django.contrib import admin
from .models import Project, Task, TaskType, TaskStatus


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['name']


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('summary', 'project', 'status', 'author', 'is_deleted', 'created', 'updated')
    list_filter = ('project', 'status', 'is_deleted')
    filter_horizontal = ('type',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    search_fields = ('title', 'description')
