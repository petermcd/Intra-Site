from django.contrib import admin

from documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """

    list_display = ("name",)
    ordering = ("name",)
