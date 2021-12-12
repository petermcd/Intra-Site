from django.db import models
from monzo.authentication import Authentication

MONZO_REDIRECT_URL = 'http://127.0.0.1:8000/admin/finance/monzo.html'


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
    name = models.CharField('Merchant', max_length=100, null=False, blank=False)
    for_lender = models.ForeignKey(Lender, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Merchant Name
        """
        return self.name


class Payment(models.Model):
    transaction_id = models.CharField('Transaction ID', max_length=50, primary_key=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.RESTRICT)
    amount = models.BigIntegerField('Amount', default=0, null=False, blank=False)
    pending = models.BooleanField('Pending', default=False, null=False, blank=False)
    when = models.DateTimeField('Created', null=False, blank=False)
    settled = models.DateTimeField('Settled', null=True, blank=True)


class DebtBalance(models.Model):
    """
    Model to host debt balances..
    """
    transaction_amount = models.BigIntegerField('Transaction Amount', null=False)
    current_balance = models.BigIntegerField('Balance', null=False, default=0)
    when = models.DateTimeField('When', blank=False, null=False)


class Loan(models.Model):
    """
    Model to host loans.
    """
    lender = models.ForeignKey(Lender, on_delete=models.RESTRICT, null=False)
    due_day = models.SmallIntegerField('Due day', null=False)
    apr = models.FloatField('APR', null=False)
    transactions = models.ManyToManyField(DebtBalance)

    def __str__(self) -> str:
        """
        To string.

        Returns:
            Lender name and amount remaining
        """
        last_transaction = self.transactions.order_by('-when')[:1]
        balance = format_money(0)
        if last_transaction:
            balance = format_money(last_transaction.current_balance)
        return f'{self.lender.name} - {balance}'


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
    client_id = models.CharField('Client ID', max_length=300)
    client_secret = models.CharField('Client Secret', max_length=300)
    owner_id = models.CharField('Owner ID', max_length=300)
    access_token = models.CharField('Access Token', max_length=300, null=True, blank=True)
    expiry = models.BigIntegerField('Expiry', null=True, blank=True)
    refresh_token = models.CharField('Refresh Token', max_length=300, null=True, blank=True)

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
        if not self.refresh_token or 1 == 1:
            monzo_auth = Authentication(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_url=MONZO_REDIRECT_URL,
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

    class Meta:
        verbose_name_plural = 'Monzo'
