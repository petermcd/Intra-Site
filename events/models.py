from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    where = models.CharField(max_length=255, blank=True, null=True)
    starting = models.DateTimeField(blank=True, null=True)
    ending = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255)
