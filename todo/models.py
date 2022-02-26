from django.db import models
from django.utils import timezone


class ToDo(models.Model):
    """
    Model for todo item.
    """
    description: models.CharField = models.CharField('ToDo Item', max_length=1000, null=False, blank=False)
    added: models.DateTimeField = models.DateTimeField('Added', blank=False, null=False, default=timezone.now)

    class Meta:
        ordering = ('description',)
