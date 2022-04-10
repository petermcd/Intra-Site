"""Models for the Finance application."""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Organisation(models.Model):
    """Organisation model."""

    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    url: models.URLField = models.URLField(max_length=200)

    def __str__(self) -> str:
        """Return the name of the organisation."""
        return str(self.name)


class Investments(models.Model):
    """Model for the Investments table."""

    organisation: models.ForeignKey = models.ForeignKey(
        Organisation, on_delete=models.CASCADE
    )
    description: models.TextField = models.TextField()
    current_value: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    date_purchased: models.DateField = models.DateField(auto_now_add=True)
    investment_document: models.FileField = models.FileField(
        upload_to="downloads/investments/", blank=True, null=True
    )

    @property
    def organisation_name(self) -> str:
        """Return the name of the organisation."""
        return "test"

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"{self.organisation.name} ({self.current_value})"


class InvestmentValue(models.Model):
    """Model for the InvestmentValue."""

    investment: models.ForeignKey = models.ForeignKey(
        Investments, on_delete=models.CASCADE
    )
    value: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    date: models.DateField = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"{self.investment.name} ({self.value})"


# Signals


@receiver(post_save, sender=Investments, dispatch_uid="update_stock_count")
def update_investment_value_log(sender, instance, **kwargs):
    """Update the investment value log."""
    new_value = InvestmentValue()
    new_value.investment = instance
    new_value.value = instance.current_value
    new_value.save()
