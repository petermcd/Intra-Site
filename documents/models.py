"""Models for the document application."""
from django.db import models


class Document(models.Model):
    """Model for Document."""

    title: models.CharField = models.CharField(max_length=200)
    description: models.CharField = models.CharField(max_length=255, blank=True)
    document: models.FileField = models.FileField(upload_to="SiteDocuments/documents/")
    uploaded_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class."""

        verbose_name = "Document"
        verbose_name_plural = "Documents"
