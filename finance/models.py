"""Models for the Finance application."""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

DEBT_TYPES = ("Loan", "Credit Card")


class Organisation(models.Model):
    """Organisation model."""

    name: models.CharField = models.CharField(max_length=100)
    url: models.URLField = models.URLField(max_length=200)

    def __str__(self) -> str:
        """Return the name of the organisation."""
        return str(self.name)

    class Meta:
        """Meta class."""

        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"


class BillType(models.Model):
    """Bill type model."""

    name: models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return the name of the bill type."""
        return str(self.name)

    class Meta:
        """Meta class."""

        verbose_name = "Bill type"
        verbose_name_plural = "Bill types"


class PaidFrom(models.Model):
    """Paid from model."""

    name: models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return the name of the paid from."""
        return str(self.name)

    class Meta:
        """Meta class."""

        verbose_name = "Paid from"
        verbose_name_plural = "Paid from"


class Bill(models.Model):
    """Bill model."""

    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    organisation: models.ForeignKey = models.ForeignKey(
        to=Organisation, on_delete=models.RESTRICT
    )
    bill_type: models.ForeignKey = models.ForeignKey(
        to=BillType, on_delete=models.CASCADE
    )
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
        to=PaidFrom, on_delete=models.RESTRICT, null=False
    )

    def __str__(self) -> str:
        """Return the name of the bill."""
        return str(self.name)

    class Meta:
        """Meta class."""

        verbose_name = "Bill"
        verbose_name_plural = "Bills"


class BillHistory(models.Model):
    """Model for the BillHistory."""

    bill: models.ForeignKey = models.ForeignKey(
        to=Bill, on_delete=models.CASCADE, null=False
    )
    current_balance: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    date: models.DateField = models.DateField(auto_now_add=True)


class Investments(models.Model):
    """Model for the Investments table."""

    organisation: models.ForeignKey = models.ForeignKey(
        to=Organisation, on_delete=models.CASCADE
    )
    description: models.TextField = models.TextField()
    current_value: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    date_purchased: models.DateField = models.DateField()
    investment_document: models.FileField = models.FileField(
        upload_to="SiteDocuments/investments/", blank=True, null=True
    )

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"{self.organisation.name} ({self.current_value})"

    @property
    def organisation_name(self) -> str:
        """Return the name of the organisation."""
        return self.organisation.name

    class Meta:
        """Meta class."""

        verbose_name = "Investment"
        verbose_name_plural = "Investments"


class InvestmentValue(models.Model):
    """Model for the InvestmentValue."""

    investment: models.ForeignKey = models.ForeignKey(
        to=Investments, on_delete=models.CASCADE
    )
    value: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    date: models.DateField = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return f"{self.investment.organisation} ({self.value})"


class Monzo(models.Model):
    """Model to store Monzo details."""

    access_token: models.CharField = models.CharField(
        max_length=250, blank=True, null=True
    )
    client_id: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    client_secret: models.CharField = models.CharField(
        max_length=100, blank=False, null=False
    )
    expiry: models.IntegerField = models.IntegerField(blank=True, null=True)
    last_fetched_datetime: models.DateTimeField = models.DateTimeField(
        blank=True, null=True
    )
    refresh_token: models.CharField = models.CharField(
        max_length=250, blank=True, null=True
    )


class MonzoMerchant(models.Model):
    """Model to store Monzo transaction merchants."""

    merchant_id: models.CharField = models.CharField(
        primary_key=True,
        max_length=50,
        blank=False,
        null=False,
    )
    name: models.CharField = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )
    for_bill: models.ForeignKey = models.ForeignKey(
        to=Bill,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class MonzoTransaction(models.Model):
    """Model to store Monzo transactions."""

    transaction_id: models.CharField = models.CharField(
        primary_key=True,
        max_length=50,
        blank=False,
        null=False,
    )
    currency: models.CharField = models.CharField(max_length=5, blank=False, null=False)
    value: models.IntegerField = models.IntegerField(blank=False, null=False)
    created: models.DateTimeField = models.DateTimeField(
        auto_created=False,
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
    )
    description: models.CharField = models.CharField(
        max_length=250, blank=False, null=False
    )
    merchant: models.ForeignKey = models.ForeignKey(
        to=MonzoMerchant,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    has_receipt: models.BooleanField = models.BooleanField(
        default=False, blank=False, null=False
    )
    for_bill: models.ForeignKey = models.ForeignKey(
        to=Bill, on_delete=models.CASCADE, blank=True, null=True
    )


# Signals


@receiver(post_save, sender=Investments, dispatch_uid="update_investment_value")
def update_investment_value_log(sender, instance, **kwargs) -> None:
    """Update the investment value log."""
    new_value = InvestmentValue()
    new_value.investment = instance
    new_value.value = instance.current_value
    new_value.save()


@receiver(post_save, sender=Bill, dispatch_uid="update_bill_history")
def update_bill_history_log(sender, instance, **kwargs) -> None:
    """Update the bill history value log."""
    if instance.bill_type.name in DEBT_TYPES:
        new_value = BillHistory()
        new_value.bill = instance
        new_value.current_balance = instance.current_balance
        new_value.save()
