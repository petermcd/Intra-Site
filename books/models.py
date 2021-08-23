from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
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
    ebook_url = models.URLField(verbose_name='eBook URL', max_length=400, default=None, blank=True)
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
