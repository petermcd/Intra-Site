# Turn off bytecode generation
import datetime
import sys
from decimal import Decimal
from typing import Dict, List, Optional

import pytz

sys.dont_write_bytecode = True

# Django specific settings
import os  # NOQA E402

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Intranet.settings")
import django  # NOQA E402

django.setup()

from monzo.authentication import Authentication  # NOQA E402
from monzo.endpoints.account import Account  # NOQA E402
from monzo.endpoints.transaction import Transaction  # NOQA E402

from finance.models import (  # NOQA E402
    Bill,
    BillAudit,
    Loan,
    LoanAudit,
    Merchant,
    Monzo,
)
from finance.views import MonzoStorage  # NOQA E402


def transaction_sorted(transaction: Transaction) -> datetime.datetime:
    """
    Sort method for transactions

    Args:
        transaction: Transaction

    Returns:
        Datetime object used for sorting
    """
    return transaction.created


class MonzoAutomation:
    __slots__ = ["_monzo_auth"]

    def __init__(self):
        """
        Standard init to initiate required objects.
        """
        monzo_config = Monzo.objects.all()[0]
        self._monzo_auth = Authentication(
            client_id=monzo_config.client_id,
            client_secret=monzo_config.client_secret,
            redirect_url=monzo_config.redirect_url,
            access_token=monzo_config.access_token,
            access_token_expiry=monzo_config.expiry,
            refresh_token=monzo_config.refresh_token,
        )
        handler = MonzoStorage()
        self._monzo_auth.register_callback_handler(handler)

    def populate_merchants(self, days: int = 7):
        """
        Populates merchants, intended to be ran when the upgrade occurs.

        Args:
            days: The number of days transactions to use to populate merchants
        """
        today = datetime.date.today()
        since_date = today - datetime.timedelta(days=days)
        since = datetime.datetime(
            year=since_date.year,
            month=since_date.month,
            day=since_date.day,
        )
        merchants = self._fetch_merchants(since=since)
        for merchant in merchants:
            self._fetch_merchant_model(
                name=merchants[merchant]["name"], logo=merchants[merchant]["logo"]
            )

    def process_transactions(self):
        """
        Process transactions to update loans and bills.
        """
        monzo = Monzo.objects.all()

        last_fetch = monzo[0].last_fetch
        if not last_fetch:
            today = datetime.date.today()
            since_date = today - datetime.timedelta(hours=24)
            since = datetime.datetime(
                year=since_date.year,
                month=since_date.month,
                day=since_date.day,
            )
        else:
            # Need to add 1 second to the datetime to account for microsecond difference
            since_date = last_fetch + datetime.timedelta(seconds=1)
            since = datetime.datetime(
                year=since_date.year,
                month=since_date.month,
                day=since_date.day,
                hour=since_date.hour,
                minute=since_date.minute,
                second=since_date.second,
            )
        account = self._fetch_accounts()
        transactions = self._fetch_transactions(account=account[0], since=since)
        transactions_sorted = sorted(transactions, key=transaction_sorted)
        monzo = Monzo.objects.all()[0]
        for transaction in transactions_sorted:
            if not transaction.merchant:
                continue
            self._process_bill_transaction(transaction=transaction)
            self._process_loan_transaction(transaction=transaction)
            monzo.last_fetch = transaction.created
        monzo.save()

    def _fetch_accounts(self, account_type: str = "uk_retail") -> List[Account]:
        """
        Fetch list of accounts from Monzo.

        Args:
            Type of account to fetch

        Returns:
            List of accounts matching account_type
        """
        return Account.fetch(auth=self._monzo_auth, account_type=account_type)

    def _fetch_merchants(
        self, since: Optional[datetime.datetime] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        Fetches merchants from a transaction list.

        Args:
            since: Datetime object for when records should be fetched from

        Returns:
            Dictionary of dictionaries
        """
        account = self._fetch_accounts()
        transactions = self._fetch_transactions(account=account[0], since=since)
        return {
            transaction.merchant["name"]: {
                "name": transaction.merchant["name"],
                "logo": transaction.merchant["logo"],
            }
            for transaction in transactions
            if transaction.merchant
        }

    def _fetch_transactions(
        self, account: Account, since: Optional[datetime.datetime] = None
    ) -> List[Transaction]:
        """
        Fetch transactions from Monzo.

        Args:
            account: The monzo account to fetch transactions for
            since: datetime to fetch transactions from

        Returns
            List of transactions
        """
        return Transaction.fetch(
            auth=self._monzo_auth,
            account_id=account.account_id,
            since=since,
            expand=["merchant"],
        )

    def _process_bill_transaction(self, transaction: Transaction):
        """
        Method to process a transaction to update items in the database.

        Args:
            transaction: Transaction
        """
        merchant = self._fetch_merchant_model(transaction.merchant["name"])
        bills = Bill.objects.filter(merchant=merchant)
        for bill in bills:
            amount = transaction.amount * -1
            bill.last_payment = transaction.created
            bill.save()

            audit = BillAudit(
                message="Updating balance from Monzo payment",
                for_bill=bill,
                transaction_value=amount,
                when=transaction.created,
            )
            audit.save()

    def _process_loan_transaction(self, transaction: Transaction):
        """
        Method to process a transaction to update items in the database.

        Args:
            transaction: Transaction
        """
        merchant = self._fetch_merchant_model(transaction.merchant["name"])
        loans = Loan.objects.filter(merchant=merchant)
        for loan in loans:
            amount = transaction.amount * -1
            if (
                not loan.variable_payment and loan.monthly_payments == amount
            ) or loan.variable_payment:
                previous_balance = loan.current_balance
                loan.current_balance = previous_balance - transaction.amount
                loan.last_payment = transaction.created
                loan.save()

                audit = LoanAudit(
                    message="Updating balance from Monzo payment",
                    for_loan=loan,
                    transaction_value=amount,
                    loan_balance=previous_balance,
                    when=transaction.created,
                )
                audit.save()

    @staticmethod
    def _fetch_merchant_model(name: str, logo: str = "") -> Merchant:
        """
        Fetch a merchant model from the database, if it does not exist create and return.

        Args:
            name: Name of the merchant
            logo: Logo for the merchant

        Returns:
            Existing merchant matching name otherwise new merchant created
        """
        try:
            merchant = Merchant.objects.get(name__exact=name)
        except Merchant.DoesNotExist:
            merchant = Merchant(name=name, logo=logo)
            merchant.save()
        return merchant

    @staticmethod
    def update_interest():
        """
        Add interest to existing loans.
        """
        loans = Loan.objects.filter(
            apr__gt=Decimal(0.0),
            current_balance__gt=0,
            start_date__lt=datetime.datetime.now(tz=pytz.UTC),
        )
        for loan in loans:
            original_balance = loan.current_balance
            yearly_interest = Decimal(loan.current_balance / 100) * loan.apr
            monthly_interest = round(yearly_interest / 12)
            new_balance = loan.current_balance + monthly_interest

            loan.current_balance = new_balance
            loan.save()

            audit = LoanAudit(
                message="Updated interest",
                for_loan=loan,
                transaction_value=monthly_interest,
                loan_balance=original_balance,
                when=datetime.datetime.now(tz=pytz.UTC),
            )
            audit.save()
