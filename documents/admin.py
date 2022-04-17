"""Admin configuration for the Documents application."""
from django.contrib import admin

from documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin for the Document model."""

    list_display = ("title", "description")
    search_fields = ("title", "description")
    ordering = ("title",)
    list_per_page = 20
