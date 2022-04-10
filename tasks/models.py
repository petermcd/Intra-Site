"""Models for the Task application."""
from django.db import models


class Task(models.Model):
    """Model for Tasks."""

    title: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    due_by: models.DateTimeField = models.DateTimeField()
    completed: models.BooleanField = models.BooleanField(default=False)
