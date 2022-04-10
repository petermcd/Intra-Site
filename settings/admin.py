"""Admin configuration for the Settings application."""
from django.contrib import admin

from settings.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Admin for the Setting model."""

    list_display = (
        "name",
        "description",
        "configured",
    )
    ordering = ("name",)
