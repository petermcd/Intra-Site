"""App configuration for Books."""
from django.apps import AppConfig


class BooksConfig(AppConfig):
    """Configuration for Books."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
