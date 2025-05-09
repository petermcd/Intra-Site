"""Admin configuration for the Tasks application."""

from django.contrib import admin

from tasks.models import Task, TaskFrequency


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin for the Task model."""

    list_display = ("title", "completed", "created_at", "due_by")
    list_filter = ("completed",)
    search_fields = ("title",)
    ordering = ("due_by",)
    date_hierarchy = "due_by"
    list_per_page = 20


@admin.register(TaskFrequency)
class TaskFrequencyAdmin(admin.ModelAdmin):
    """Admin for the TaskFrequency Admin."""

    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)
