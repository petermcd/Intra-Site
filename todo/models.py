from django.db import models
from django.utils import timezone


class ToDo(models.Model):
    description = models.CharField('ToDo Item', max_length=1000, null=False, blank=False)
    added = models.DateTimeField('Added', blank=False, null=False, default=timezone.now)
