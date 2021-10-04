from django.db import models


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
