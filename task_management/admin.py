from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_type', 'status', 'created_at')
    list_filter = ('status', 'task_type')
    search_fields = ('name', 'description')
    filter_horizontal = ('assigned_users',)
    readonly_fields = ('created_at',)

