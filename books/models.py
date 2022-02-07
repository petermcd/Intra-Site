from django.db import models

from Intranet.misc import OverwriteStorage


def content_file_name(instance, filename) -> str:
    """
    Create the book filename and path

    Args:
        instance: Model instance
        filename: uploaded filename

    Returns:
        New path and filename as a string
    """
    path: str = 'downloads/books/'
    ext: str = filename.split('.')[-1]
    new_filename: str = f'{path}{instance.isbn10}.{ext}'
    if instance.isbn10.startswith('00000'):
        new_filename = f'{path}{instance.title}.{ext}'
    return new_filename


class Author(models.Model):
    """
    Model for Author.
    """
    name: models.CharField = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return str(self.name)


class Book(models.Model):
    """
    Model for Book.
    """
    title: models.CharField = models.CharField(max_length=200)
    subtitle: models.CharField = models.CharField(max_length=500, default=None, blank=True)
    authors: models.ManyToManyField = models.ManyToManyField(Author)
    publisher: models.CharField = models.CharField(max_length=200)
    published: models.DateField = models.DateField()
    isbn10: models.CharField = models.CharField(max_length=10, unique=True)
    isbn13: models.CharField = models.CharField(max_length=13, unique=True)
    description: models.CharField = models.CharField(max_length=5000)
    pages: models.IntegerField = models.IntegerField()
    thumbnail: models.URLField = models.URLField(max_length=255, default=None, blank=True)
    ebook: models.FileField = models.FileField(storage=OverwriteStorage, null=True, blank=True, upload_to=content_file_name)
    read: models.BooleanField = models.BooleanField(default=False)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return str(self.title)
