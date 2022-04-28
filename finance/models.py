"""Models for the Finance application."""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Organisation(models.Model):
    """Organisation model."""

    name: models.CharField = models.CharField(max_length=100)
    url: models.URLField = models.URLField(max_length=200)

    class Meta:
        """Meta class."""

        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"

    def __str__(self) -> str:
        """Return the name of the organisation."""
        return str(self.name)


class BillType(models.Model):
    """Bill type model."""

    name: models.CharField = models.CharField(max_length=100)

    class Meta:
        """Meta class."""

        verbose_name = "Bill type"
        verbose_name_plural = "Bill types"

    def __str__(self) -> str:
        """Return the name of the bill type."""
        return str(self.name)


class PaidFrom(models.Model):
    """Paid from model."""

    name: models.CharField = models.CharField(max_length=100)

    class Meta:
        """Meta class."""

        verbose_name = "Paid from"
        verbose_name_plural = "Paid from"

    def __str__(self) -> str:
        """Return the name of the paid from."""
        return str(self.name)


class Bill(models.Model):
    """Bill model."""

    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    organisation: models.ForeignKey = models.ForeignKey(
        Organisation, on_delete=models.RESTRICT
    )
    bill_type: models.ForeignKey = models.ForeignKey(BillType, on_delete=models.CASCADE)
    due_day: models.SmallIntegerField = models.SmallIntegerField(default=1)
    monthly_payments: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    current_balance: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    apr: models.DecimalField = models.DecimalField(
        max_digits=5, decimal_places=3, default=0.0
    )
    variable_payment: models.BooleanField = models.BooleanField(default=False)
    start_date: models.DateTimeField = models.DateTimeField(blank=True, null=True)
    last_payment: models.DateTimeField = models.DateTimeField(blank=True, null=True)
    paid_from: models.ForeignKey = models.ForeignKey(
        PaidFrom, on_delete=models.RESTRICT, null=False
    )

    class Meta:
        """Meta class."""

        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    def __str__(self) -> str:
        """Return the name of the bill."""
        return str(self.name)


class BillHistory(models.Model):
    """Model for the BillHistory."""

    bill: models.ForeignKey = models.ForeignKey(
        Bill, on_delete=models.CASCADE, null=False
    )
    current_balance: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    date: models.DateField = models.DateField(auto_now_add=True)


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
        upload_to="SiteDocuments/investments/", blank=True, null=True
    )

    class Meta:
        """Meta class."""

        verbose_name = "Investment"
        verbose_name_plural = "Investments"

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


@receiver(post_save, sender=Investments, dispatch_uid="update_investment_value")
def update_investment_value_log(sender, instance, **kwargs):
    """Update the investment value log."""
    new_value = InvestmentValue()
    new_value.investment = instance
    new_value.value = instance.current_value
    new_value.save()


@receiver(post_save, sender=Bill, dispatch_uid="update_bill_history")
def update_bill_history_log(sender, instance, **kwargs):
    """Update the bill history value log."""
    if instance.bill_type.name.lower() in ("loan", "credit card"):
        new_value = BillHistory()
        new_value.bill = instance
        new_value.current_balance = instance.current_balance
        new_value.save()
