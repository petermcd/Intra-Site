from datetime import date, datetime
from typing import List, Union

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Company(models.Model):

    name = models.CharField('Company', max_length=30)
    url = models.URLField('Website', max_length=255)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return self.name


class Bill(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_day = models.IntegerField()
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return f'{self.company} - {self.payment_amount_clean}'

    @property
    def payment_amount_clean(self) -> str:
        """
        Fetch the payment amount formatted in pounds and pence.

        Return:
            Formatted payment amount
        """
        return format_money(self.payment_amount)

    @property
    def calculated_payment_amount(self) -> int:
        """
        Fetch the amount to be paid.

        Return:
            payment amount or current balance whichever is the least
        """
        return self.payment_amount

    @staticmethod
    def type() -> str:
        """
        Fetch the type of payment.

        Return:
            Payment type
        """
        return 'bill'


class Debt(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    starting_balance = models.IntegerField()
    current_balance = models.IntegerField()
    interest_rate = models.FloatField()
    payment_amount = models.IntegerField()
    payment_day = models.IntegerField()
    description = models.CharField(max_length=500)

    def has_outstanding_balance(self) -> bool:
        """
        Check if the debt has an outstanding balance.

        Return:
            True if an outstanding balance exists otherwise False
        """
        return self.current_balance > 0

    def __str__(self) -> str:
        """
        Standard to string.

        Return:
            String representation of the object
        """
        return f'{self.company.name} - {format_money(self.current_balance)}'

    @property
    def name(self) -> str:
        """
        Fetch the name of the company associated with a debt.

        Return:
            name of the company associated with the debt
        """
        return self.company.name

    @property
    def payment_amount_clean(self) -> str:
        """
        Fetch the payment amount formatted in pounds and pence.

        Return:
            Formatted payment amount
        """
        return format_money(self.calculated_payment_amount)

    @property
    def calculated_payment_amount(self) -> int:
        """
        Fetch the amount to be paid.

        Return:
            payment amount or current balance whichever is the least
        """
        payment = self.payment_amount
        if self.payment_amount > self.current_balance:
            payment = self.current_balance
        return payment

    @property
    def current_balance_clean(self) -> str:
        """
        Fetch the current balance formatted in pounds and pence.

        Return:
            Formatted current value
        """
        return format_money(self.current_balance)

    @property
    def remaining_payment_count(self) -> int:
        """
        Fetch the number of remaining payments.

        Return:
            Number of remaining payments
        """
        return len(self.remaining_payments())

    def remaining_payments(self):
        """
        Generate a list of remaining payments based on the current remaining balance and interest rate.

        Return:
            List of remaining payments
        """
        payments = []
        if self.payment_amount == 0:
            return payments
        monthly_interest_rate = self.interest_rate / 12
        current_balance = self.current_balance
        monthly_payments = self.payment_amount

        today = date.today()
        next_payment = datetime(today.year, today.month, self.payment_day)
        if today.day >= self.payment_day:
            next_payment = add_month(self.payment_day, next_payment)
        while current_balance > 0:
            if current_balance < monthly_payments:
                monthly_payments = current_balance
            payment = {
                'date': next_payment.strftime('%d/%m/%y'),
                'balance': format_money(current_balance),
                'payment': format_money(monthly_payments),
            }
            remaining_pre_interest = current_balance - monthly_payments
            interest = int(
                remaining_pre_interest * (monthly_interest_rate / 100)
            )
            current_balance = remaining_pre_interest + interest
            payment['interest'] = format_money(interest)
            payment['remaining_balance'] = format_money(current_balance)
            payments.append(payment)
            next_payment = add_month(self.payment_day, next_payment)
        return payments

    @staticmethod
    def type() -> str:
        """
        Fetch the type of payment.

        Return:
            Payment type
        """
        return 'debt'


class Investment(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    value = models.IntegerField()

    @property
    def value_clean(self) -> str:
        """
        Fetch the value of the investment formatted

        Return:
            Formatted value
        """
        return format_money(self.value)


class InvestmentHistory(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    value = models.IntegerField()
    at = models.DateField(auto_now_add=True)

    @property
    def value_clean(self) -> str:
        """
        Fetch the value of the investment formatted

        Return:
            Formatted value
        """
        return format_money(self.value)


class Payments:
    @staticmethod
    def monthly_payments() -> List[Union[Bill, Debt]]:
        """
        Fetch Bills and debts that have payments to be paid in the current month

        Return:
            List of Bills and Debts that fit the criteria
        """
        payments = [bill for bill in Bill.objects.all()]
        today = now()
        for debt in Debt.objects.filter(current_balance__gt=0, payment_amount__gt=0, start_date__lte=today):
            payments.append(debt)
        payments.sort(key=Payments._sort)
        return payments

    @staticmethod
    def _sort(elem) -> str:
        """
        Specifies the object attribute to order items by.

        Return:
            Value of the attribute to order by
        """
        return elem.payment_day


def format_money(value: int) -> str:
    """
    Convert a financial value from pence to pounds and pence to 2 decimal places.

    Return: Money formatted to 2 decimal places
    """
    return f'{value / 100:.2f}'


def add_month(payment_day, payment_date) -> datetime:
    """
    Add a month to identify the next payment date.

    Args:
        payment_day: Day a payment is usually taken
        payment_date: date of the last payment

    Return:
        Datetime object containing the date of the next payment
    """
    max_days = [
        0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ]
    day = payment_day
    month = payment_date.month + 1
    year = payment_date.year
    if month > 12:
        month = 1
        year += 1
    day = min(day, max_days[month])
    return datetime(year, month, day)


@receiver(post_save, sender=Investment)
def investment_update_history(sender, instance, **kwargs):
    """
    Add an entry into the history when an investment is updated.

    Args:
        sender: Object that created the request
        instance: Object being updated
        kwargs: Not used but required for the API
    """
    history_item = InvestmentHistory()
    history_item.investment = instance
    history_item.value = instance.value
    history_item.save()
