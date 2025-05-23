"""Models for the books application."""

from django.db import models

from intranet.helpers import OverwriteStorageName


def content_file_name(instance, filename) -> str:
    """
    Create the book filename and path.

    Args:
        instance: Model instance
        filename: uploaded filename

    Returns:
        New path and filename as a string
    """
    path: str = "SiteDocuments/books/"
    ext: str = filename.split(".")[-1]
    new_filename: str = f"{path}{instance.isbn10}.{ext}"
    if instance.isbn10.startswith("00000"):
        new_filename = f"{path}{instance.title}.{ext}"
    return new_filename


class Author(models.Model):
    """Model for Author."""

    name: models.CharField = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        """
        Convert object to a string.

        Return:
            String representation of the object
        """
        return str(self.name)

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("name",)
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """Model for Book."""

    title: models.CharField = models.CharField(max_length=200)
    subtitle: models.CharField = models.CharField(
        max_length=500, default=None, blank=True
    )
    authors: models.ManyToManyField = models.ManyToManyField(Author)
    publisher: models.CharField = models.CharField(max_length=200)
    published: models.DateField = models.DateField()
    isbn10: models.CharField = models.CharField(max_length=10, unique=True)
    isbn13: models.CharField = models.CharField(max_length=13, unique=True)
    description: models.CharField = models.CharField(max_length=5000)
    thumbnail: models.URLField = models.URLField(
        max_length=255, default=None, blank=True
    )
    ebook: models.FileField = models.FileField(
        storage=OverwriteStorageName, null=True, blank=True, upload_to=content_file_name
    )
    read: models.BooleanField = models.BooleanField(default=False)

    def __str__(self) -> str:
        """
        Convert object to a string.

        Return:
            String representation of the object
        """
        return str(self.title)

    class Meta:
        """Meta class."""

        ordering = ("title",)
        verbose_name = "Book"
        verbose_name_plural = "Books"
