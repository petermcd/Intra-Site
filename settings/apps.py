"""App configuration for Settings."""
from django.apps import AppConfig


class SettingsConfig(AppConfig):
    """Configuration for the settings application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "settings"
