"""App configuration for Todo."""
from django.apps import AppConfig


class TodoConfig(AppConfig):
    """Configuration for Todo."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "todo"
