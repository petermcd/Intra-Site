"""Models for the Task application."""
from django.db import models


class Task(models.Model):
    """Model for Tasks."""

    title: models.CharField = models.CharField(max_length=200, blank=False, null=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    due_by: models.DateTimeField = models.DateTimeField()
    completed: models.BooleanField = models.BooleanField(default=False)
    frequency: models.ForeignKey = models.ForeignKey(
        to="TaskFrequency", on_delete=models.RESTRICT, blank=True, null=True
    )

    class Meta:
        """Meta class."""

        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        """Return the task name."""
        return self.title


class TaskFrequency(models.Model):
    """Model for Tasks."""

    title: models.CharField = models.CharField(max_length=200)
    days_to_add: models.IntegerField = models.IntegerField(default=0)
    months_to_add: models.IntegerField = models.IntegerField(default=0)
    years_to_add: models.IntegerField = models.IntegerField(default=0)

    class Meta:
        """Meta class."""

        verbose_name = "Task Frequency"
        verbose_name_plural = "Task Frequencies"

    def __str__(self):
        """Return the task frequency name."""
        return self.title
