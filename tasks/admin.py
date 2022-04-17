"""Admin configuration for the Tasks application."""
from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin for the Task model."""

    list_display = ("title", "description", "completed", "created_at", "due_by")
    list_filter = ("completed",)
    search_fields = ("title", "description")
    ordering = ("due_by",)
    date_hierarchy = "due_by"
    list_per_page = 20
