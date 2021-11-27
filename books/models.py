from django.db import models

from Intranet.misc import OverwriteStorage


class Author(models.Model):
    """
    Model for Author.
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return self.name


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'books/{instance.isbn10}.{ext}'
    if instance.isbn10 == '0000000000':
        filename = f'books/{instance.title}.{ext}'
    return filename


class Book(models.Model):
    """
    Model for Book.
    """
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, default=None, blank=True)
    authors = models.ManyToManyField(Author)
    publisher = models.CharField(max_length=200)
    published = models.DateField()
    isbn10 = models.CharField(max_length=10, unique=True)
    isbn13 = models.CharField(max_length=13, unique=True)
    description = models.CharField(max_length=5000)
    pages = models.IntegerField()
    thumbnail = models.URLField(max_length=255, default=None, blank=True)
    ebook = models.FileField(storage=OverwriteStorage, null=True, blank=True, upload_to=content_file_name)
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return self.title
