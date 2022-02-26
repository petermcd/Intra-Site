from django.db import models

from Intranet.misc import OverwriteStorage


def document_file_name(instance, filename) -> str:
    """
    Create filename for a document.

    Args:
        instance: Model class uploading the file
        filename: The name of the file uploaded

    Returns: String containing the new filename
    """
    return f'downloads/documents/{filename}'


class Document(models.Model):
    """
    Model for Document.
    """
    name: models.CharField = models.CharField(max_length=200)
    document: models.FileField = models.FileField(
        storage=OverwriteStorage,
        null=True, blank=True,
        upload_to=document_file_name
    )
    description: models.CharField = models.CharField(max_length=1000, verbose_name='Description')

    class Meta:
        ordering = ('name',)
