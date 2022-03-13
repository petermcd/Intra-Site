"""Models for Finance."""
from django.db import models
from django.utils.safestring import mark_safe
from monzo.authentication import Authentication


class PaidFrom(models.Model):
    """Model for paid from."""

    name: models.CharField = models.CharField(
        "Paid From", max_length=100, null=False, blank=False
    )

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Paid from name
        """
        return str(self.name)

    class Meta:
        """Class to correct the order of the items in the admin panel and the pluralisation of admin links."""

        verbose_name = "Paid From"
        verbose_name_plural = "Paid From"
        ordering = ("name",)


class Lender(models.Model):
    """Model to host lender details."""

    name: models.CharField = models.CharField(
        "Lender", max_length=50, unique=True, null=False
    )
    url: models.URLField = models.URLField("Website", max_length=255)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name
        """
        return str(self.name)

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("name",)


class Merchant(models.Model):
    """Model for merchant."""

    name: models.CharField = models.CharField(
        "Merchant", unique=True, max_length=100, null=False, blank=False
    )
    logo: models.URLField = models.URLField("Logo", null=True, blank=True)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Merchant Name
        """
        return str(self.name)

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("name",)


class Bill(models.Model):
    """Model to host bills."""

    company: models.ForeignKey = models.ForeignKey(
        Lender, on_delete=models.RESTRICT, null=False
    )
    due_day: models.SmallIntegerField = models.SmallIntegerField(
        "Due day", null=False, default=1
    )
    monthly_payments: models.BigIntegerField = models.BigIntegerField(
        "Monthly Payments", null=False, default=0
    )
    merchant: models.ForeignKey = models.ForeignKey(
        Merchant, on_delete=models.RESTRICT, blank=True, null=True
    )
    variable_payment: models.BooleanField = models.BooleanField(
        "Variable Payment", default=False
    )
    last_payment: models.DateTimeField = models.DateTimeField(
        "Last Payment", blank=True, null=True
    )
    notes: models.CharField = models.CharField(
        "Notes", max_length=300, null=False, blank=False
    )
    paid_from: models.ForeignKey = models.ForeignKey(
        PaidFrom, on_delete=models.RESTRICT, null=False
    )

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name and amount remaining
        """
        return f"{self.company.name}"

    @property
    def merchant_configured(self) -> str:
        """
        Property to identify if the loan is matched to a merchant.

        Returns:
            No if not, otherwise an empty string
        """
        return "" if bool(self.merchant) else "No"

    @property
    def formatted_monthly_payment(self) -> str:
        """
        Fetch the monthly payment formatted.

        Returns:
            Monthly payment formatted
        """
        return format_money(money=int(self.monthly_payments))

    @property
    def bill_type(self) -> str:
        """
        Property for the bill type.

        Returns:
            bill type
        """
        return "bill"

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("company",)


class BillAudit(models.Model):
    """Model to host bill audit."""

    message: models.CharField = models.CharField(
        "Message", max_length=100, null=False, blank=False
    )
    transaction_value: models.BigIntegerField = models.BigIntegerField(
        "Transaction Value", null=False, blank=False
    )
    for_bill: models.ForeignKey = models.ForeignKey(
        Bill, on_delete=models.RESTRICT, blank=False, null=False
    )
    when: models.DateTimeField = models.DateTimeField("When", blank=False, null=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Summary of record
        """
        return f"{self.for_bill} - {self.message} - {self.transaction_value}"

    @property
    def formatted_transaction_value(self) -> str:
        """
        Fetch formatted transaction value.

        Returns:
            Formatted transaction value
        """
        return format_money(int(self.transaction_value))

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("when",)


class Loan(models.Model):
    """Model to host loans."""

    lender: models.ForeignKey = models.ForeignKey(
        Lender, on_delete=models.RESTRICT, null=False
    )
    due_day: models.SmallIntegerField = models.SmallIntegerField(
        "Due day", null=False, default=1
    )
    monthly_payments: models.BigIntegerField = models.BigIntegerField(
        "Monthly Payments", null=False, default=0
    )
    current_balance: models.BigIntegerField = models.BigIntegerField(
        "Balance", null=False, default=0
    )
    apr: models.DecimalField = models.DecimalField(
        "APR", max_digits=5, decimal_places=3, null=False, default=0.0
    )
    merchant: models.ForeignKey = models.ForeignKey(
        Merchant, on_delete=models.RESTRICT, blank=True, null=True
    )
    variable_payment: models.BooleanField = models.BooleanField(
        "Variable Payment", default=False
    )
    start_date: models.DateTimeField = models.DateTimeField(
        "Start Date", blank=True, null=True
    )
    last_payment: models.DateTimeField = models.DateTimeField(
        "Last Payment", blank=True, null=True
    )
    notes: models.CharField = models.CharField(
        "Notes", max_length=300, null=False, blank=False
    )
    paid_from: models.ForeignKey = models.ForeignKey(
        PaidFrom, on_delete=models.RESTRICT, null=False
    )

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name and amount remaining
        """
        return f"{self.lender.name} - {format_money(int(self.current_balance))}"

    @property
    def merchant_configured(self) -> str:
        """
        Property to identify if the loan is matched to a merchant.

        Returns:
            No if not, otherwise an empty string
        """
        return "" if bool(self.merchant) else "No"

    @property
    def formatted_monthly_payment(self) -> str:
        """
        Fetch the monthly payment formatted.

        Returns:
            Monthly payment formatted
        """
        return format_money(money=int(self.monthly_payments))

    @property
    def formatted_current_balance(self) -> str:
        """
        Fetch the current balance formatted.

        Returns:
            Current balance formatted
        """
        return format_money(money=int(self.current_balance))

    @property
    def bill_type(self) -> str:
        """
        Property for the bill type.

        Returns:
            bill type
        """
        return "loan"

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("lender",)


class LoanAudit(models.Model):
    """Model to host loan audit."""

    message: models.CharField = models.CharField(
        "Message", max_length=100, null=False, blank=False
    )
    transaction_value: models.BigIntegerField = models.BigIntegerField(
        "Transaction Value", null=False, blank=False
    )
    for_loan: models.ForeignKey = models.ForeignKey(
        Loan, on_delete=models.RESTRICT, blank=False, null=False
    )
    loan_balance: models.BigIntegerField = models.BigIntegerField(
        "Loan Balance", null=False, default=0
    )
    when: models.DateTimeField = models.DateTimeField("When", blank=False, null=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Summary of record
        """
        return f"{self.for_loan} - {self.message} - {self.transaction_value}"

    @property
    def formatted_transaction_value(self) -> str:
        """
        Fetch formatted transaction value.

        Returns:
            Formatted transaction value
        """
        return format_money(int(self.transaction_value))

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("when",)


def format_money(money: int, symbol_left: str = "£", symbol_right: str = "") -> str:
    """
    Format a given amount.

    Args:
        money: The amount to be formatted
        symbol_left: Currency left symbol
        symbol_right: Currency right symbol

    Returns:
         money converted with symbol
    """
    return f"{symbol_left}{money/100:.2f}{symbol_right}"


class Monzo(models.Model):
    """Model for Monzo settings."""

    site: models.CharField = models.CharField("Site", max_length=100)
    client_id: models.CharField = models.CharField("Client ID", max_length=300)
    client_secret: models.CharField = models.CharField("Client Secret", max_length=300)
    owner_id: models.CharField = models.CharField("Owner ID", max_length=300)
    access_token: models.CharField = models.CharField(
        "Access Token", max_length=300, null=True, blank=True
    )
    expiry: models.BigIntegerField = models.BigIntegerField(
        "Expiry", null=True, blank=True
    )
    refresh_token: models.CharField = models.CharField(
        "Refresh Token", max_length=300, null=True, blank=True
    )
    last_fetch: models.DateTimeField = models.DateTimeField(
        "Last Fetch", blank=True, null=True
    )

    @property
    def linked(self):
        """
        Property to identify if Monzo is linked.

        Returns:
            Yes if linked otherwise No
        """
        return (
            "Yes" if all([self.access_token, self.expiry, self.refresh_token]) else "No"
        )

    def output_link_url(self) -> str:
        """
        Output the link URL.

        Returns:
            Link as a string
        """
        return mark_safe(self.link_url())

    def save(self, *args, **kwargs):
        """Override sae method to ensure we only have one record."""
        if not self.pk and Monzo.objects.exists():
            raise ValueError("Monzo configuration already exists")
        super().save(*args, **kwargs)

    def link_url(self) -> str:
        """
        Property for the link.

        Returns:
             The link to authenticate Monzo otherwise 'Linked
        """
        if not self.refresh_token:
            monzo_auth = Authentication(
                client_id=str(self.client_id),
                client_secret=str(self.client_secret),
                redirect_url=self.redirect_url,
                access_token=str(self.access_token),
            )
            return f'<a href="{monzo_auth.authentication_url}">LINK</a>'
        return "Linked"

    def __str__(self):
        """
        To string for Monzo.

        Returns:
            The name of the Event
        """
        return "Monzo Configuration"

    @property
    def redirect_url(self) -> str:
        """
        Fetch the redirect url.

        Returns: redirect url as a string
        """
        return f"{self.site}/admin/finance/monzo.html"

    class Meta:
        """Class to correct pluralisation of admin links."""

        verbose_name_plural = "Monzo"


class Investment(models.Model):
    """Model for investment."""

    company: models.ForeignKey = models.ForeignKey(
        Lender, on_delete=models.RESTRICT, null=False
    )
    value: models.BigIntegerField = models.BigIntegerField(
        "Value", null=False, default=0
    )
    notes: models.CharField = models.CharField(
        "Notes", max_length=300, null=False, blank=False
    )

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Paid from name
        """
        return f"{self.company} - {self.formatted_value}"

    @property
    def formatted_value(self) -> str:
        """
        Fetch the monthly payment formatted.

        Returns:
            Monthly payment formatted
        """
        return format_money(money=int(self.value))

    class Meta:
        """Class to correct the order of the items in the admin panel."""

        ordering = ("company",)
