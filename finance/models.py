from datetime import date, datetime

from django.db import models


class Currency(models.Model):
    name = models.CharField('Name', max_length=50)
    shortname = models.CharField('Shortname', max_length=3)
    symbol = models.CharField('Symbol', max_length=1)

    def __str__(self) -> str:
        return self.shortname


class Company(models.Model):

    name = models.CharField('Company', max_length=30)
    url = models.URLField('Website', max_length=255)

    def __str__(self):
        return self.name


class Bill(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_day = models.IntegerField()
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f'{self.company} - {self.payment_amount_clean}'

    @property
    def payment_amount_clean(self) -> str:
        return format_money(self.payment_amount)

    @property
    def calculated_payment_amount(self) -> int:
        return self.payment_amount

    @staticmethod
    def type() -> str:
        return 'bill'


class Debt(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    start_date = models.DateField()
    starting_balance = models.IntegerField()
    current_balance = models.IntegerField()
    interest_rate = models.FloatField()
    payment_amount = models.IntegerField()
    payment_day = models.IntegerField()
    description = models.CharField(max_length=500)

    def has_outstanding_balance(self):
        return self.current_balance > 0

    def __str__(self) -> str:
        return f'{self.company.name} - {format_money(self.current_balance)}'

    @property
    def name(self) -> str:
        return self.company.name

    @property
    def payment_amount_clean(self) -> str:
        return format_money(self.calculated_payment_amount)

    @property
    def calculated_payment_amount(self) -> int:
        payment = self.payment_amount
        if self.payment_amount > self.current_balance:
            payment = self.current_balance
        return payment

    @property
    def current_balance_clean(self) -> str:
        return format_money(self.current_balance)

    @property
    def remaining_payment_count(self) -> int:
        return len(self.remaining_payments())

    def remaining_payments(self):
        payments = []
        if self.payment_amount == 0:
            return payments
        monthly_interest_rate = self.interest_rate / 12
        current_balance = self.current_balance
        monthly_payments = self.payment_amount

        today = date.today()
        next_payment = datetime(today.year, today.month, today.day)
        if today.day >= self.payment_day:
            next_payment = add_month(next_payment)
        while current_balance > 0:
            if current_balance < monthly_payments:
                monthly_payments = current_balance
            payment = {
                'date': next_payment.strftime("%d/%m/%Y"),
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
            next_payment = add_month(next_payment)
        return payments

    @staticmethod
    def type() -> str:
        return 'debt'


class Payments:
    @staticmethod
    def monthly_payments():
        payments = list()
        for bill in Bill.objects.all():
            payments.append(bill)
        for debt in Debt.objects.all():
            payments.append(debt)
        payments.sort(key=Payments._sort)
        return payments

    @staticmethod
    def _sort(elem):
        return elem.payment_day


def format_money(value: int) -> str:
    return f'{value / 100:.2f}'


def add_month(payment_date):
    day = payment_date.day
    month = payment_date.month + 1
    year = payment_date.year
    if month > 12:
        month = 1
        year += 1
    return datetime(year, month, day)
