from django.db import models
from monzo.authentication import Authentication


class PaidFrom(models.Model):
    name = models.CharField('Paid From', max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Paid from name
        """
        return self.name

    class Meta:
        verbose_name = 'Paid From'
        verbose_name_plural = 'Paid From'


class Lender(models.Model):
    """
    Model to host lender details.
    """
    name = models.CharField('Lender', max_length=50, unique=True, null=False)
    url = models.URLField('Website', max_length=255)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name
        """
        return self.name


class Merchant(models.Model):
    name = models.CharField('Merchant', unique=True, max_length=100, null=False, blank=False)
    logo = models.URLField('Logo', null=True, blank=True)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Merchant Name
        """
        return self.name


class Bill(models.Model):
    """
    Model to host bills.
    """
    company = models.ForeignKey(Lender, on_delete=models.RESTRICT, null=False)
    due_day = models.SmallIntegerField('Due day', null=False, default=1)
    monthly_payments = models.BigIntegerField('Monthly Payments', null=False, default=0)
    merchant = models.ForeignKey(Merchant, on_delete=models.RESTRICT, blank=True, null=True)
    variable_payment = models.BooleanField('Variable Payment', default=False)
    last_payment = models.DateTimeField('Last Payment', blank=True, null=True)
    notes = models.CharField('Notes', max_length=300, null=False, blank=False)
    paid_from = models.ForeignKey(PaidFrom, on_delete=models.RESTRICT, null=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name and amount remaining
        """
        return f'{self.company.name}'

    @property
    def merchant_configured(self) -> str:
        return '' if bool(self.merchant) else 'No'

    @property
    def formatted_monthly_payment(self) -> str:
        """
        Fetch the monthly payment formatted.

        Returns:
            Monthly payment formatted
        """
        return format_money(money=self.monthly_payments)

    @property
    def bill_type(self) -> str:
        """
        Property for the bill type.

        Returns:
            bill type
        """
        return 'bill'


class BillAudit(models.Model):
    """
    Model to host bill audit.
    """
    message = models.CharField('Message', max_length=100, null=False, blank=False)
    transaction_value = models.BigIntegerField('Transaction Value', null=False, blank=False)
    for_bill = models.ForeignKey(Bill, on_delete=models.RESTRICT, blank=False, null=False)
    when = models.DateTimeField('When', blank=False, null=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Summary of record
        """
        return f'{self.for_bill} - {self.message} - {self.transaction_value}'

    @property
    def formatted_transaction_value(self) -> str:
        """
        Fetch formatted transaction value.

        Returns:
            Formatted transaction value
        """
        return format_money(self.transaction_value)


class Loan(models.Model):
    """
    Model to host loans.
    """
    lender = models.ForeignKey(Lender, on_delete=models.RESTRICT, null=False)
    due_day = models.SmallIntegerField('Due day', null=False, default=1)
    monthly_payments = models.BigIntegerField('Monthly Payments', null=False, default=0)
    current_balance = models.BigIntegerField('Balance', null=False, default=0)
    apr = models.DecimalField('APR', max_digits=5, decimal_places=3, null=False,  default=0.0)
    merchant = models.ForeignKey(Merchant, on_delete=models.RESTRICT, blank=True, null=True)
    variable_payment = models.BooleanField('Variable Payment', default=False)
    start_date = models.DateTimeField('Start Date', blank=True, null=True)
    last_payment = models.DateTimeField('Last Payment', blank=True, null=True)
    notes = models.CharField('Notes', max_length=300, null=False, blank=False)
    paid_from = models.ForeignKey(PaidFrom, on_delete=models.RESTRICT, null=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name and amount remaining
        """
        return f'{self.lender.name} - {format_money(self.current_balance)}'

    @property
    def merchant_configured(self) -> str:
        return '' if bool(self.merchant) else 'No'

    @property
    def formatted_monthly_payment(self) -> str:
        """
        Fetch the monthly payment formatted.

        Returns:
            Monthly payment formatted
        """
        return format_money(money=self.monthly_payments)

    @property
    def formatted_current_balance(self) -> str:
        """
        Fetch the current balance formatted.

        Returns:
            Current balance formatted
        """
        return format_money(money=self.current_balance)

    @property
    def bill_type(self) -> str:
        """
        Property for the bill type.

        Returns:
            bill type
        """
        return 'loan'


class LoanAudit(models.Model):
    """
    Model to host loan audit.
    """
    message = models.CharField('Message', max_length=100, null=False, blank=False)
    transaction_value = models.BigIntegerField('Transaction Value', null=False, blank=False)
    for_loan = models.ForeignKey(Loan, on_delete=models.RESTRICT, blank=False, null=False)
    loan_balance = models.BigIntegerField('Loan Balance', null=False, default=0)
    when = models.DateTimeField('When', blank=False, null=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Summary of record
        """
        return f'{self.for_loan} - {self.message} - {self.transaction_value}'

    @property
    def formatted_transaction_value(self) -> str:
        """
        Fetch formatted transaction value.

        Returns:
            Formatted transaction value
        """
        return format_money(self.transaction_value)


def format_money(money: int, symbol_left: str = '£', symbol_right: str = '') -> str:
    """
    Format a given amount.

    Args:
        money: The amount to be formatted
        symbol_left: Currency left symbol
        symbol_right: Currency right symbol

    Returns:
         money converted with symbol
    """
    return f'{symbol_left}{money/100:.2f}{symbol_right}'


class Monzo(models.Model):
    site = models.CharField('Site', max_length=100)
    client_id = models.CharField('Client ID', max_length=300)
    client_secret = models.CharField('Client Secret', max_length=300)
    owner_id = models.CharField('Owner ID', max_length=300)
    access_token = models.CharField('Access Token', max_length=300, null=True, blank=True)
    expiry = models.BigIntegerField('Expiry', null=True, blank=True)
    refresh_token = models.CharField('Refresh Token', max_length=300, null=True, blank=True)
    last_fetch = models.DateTimeField('Last Fetch', blank=True, null=True)

    @property
    def linked(self):
        """
        Property to identify if Monzo is linked.

        Returns:
            Yes if linked otherwise No
        """
        return 'Yes' if all([self.access_token, self.expiry, self.refresh_token]) else 'No'

    def save(self, *args, **kwargs):
        """
        Override sae method to ensure we only have one record.
        """
        if not self.pk and Monzo.objects.exists():
            raise ValueError('Monzo configuration already exists')
        super(Monzo, self).save(*args, **kwargs)

    def link_url(self) -> str:
        """
        Property for the link.

        Returns:
             The link to authenticate Monzo otherwise 'Linked
        """
        if not self.refresh_token:
            monzo_auth = Authentication(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_url=self.redirect_url,
                access_token=self.access_token,
            )
            return f'<a href="{monzo_auth.authentication_url}">LINK</a>'
        return 'Linked'

    def __str__(self):
        """
        To string for Monzo.

        Returns:
            The name of the Event
        """
        return 'Monzo Configuration'

    @property
    def redirect_url(self) -> str:
        """
        Fetch the redirect url.

        Returns: redirect url as a string
        """
        return f'{self.site}/admin/finance/monzo.html'

    class Meta:
        verbose_name_plural = 'Monzo'


class Investment(models.Model):
    company = models.ForeignKey(Lender, on_delete=models.RESTRICT, null=False)
    value = models.BigIntegerField('Value', null=False, default=0)
    notes = models.CharField('Notes', max_length=300, null=False, blank=False)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Paid from name
        """
        return f'{self.company} - {self.formatted_value}'

    @property
    def formatted_value(self) -> str:
        """
        Fetch the monthly payment formatted.

        Returns:
            Monthly payment formatted
        """
        return format_money(money=self.value)
