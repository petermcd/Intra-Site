"""Models for the Settings application."""

from django.db import models


class Setting(models.Model):
    """Model for the Settings table."""

    name: models.CharField = models.CharField(max_length=100, unique=True)
    value: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    description: models.CharField = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Return the name of the setting.

        Returns:
            The name of the setting
        """
        return str(self.name)

    def configured(self) -> str:
        """
        Identify if the setting has been configured.

        Returns:
            Yes if configured otherwise No
        """
        return "Yes" if self.value else "No"

    class Meta:
        """Meta class."""

        ordering = ("name",)
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
