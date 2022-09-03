"""Class to support Monzo automation."""
from datetime import datetime, timedelta
from typing import Union

from monzo.authentication import Authentication
from monzo.endpoints.account import Account
from monzo.endpoints.transaction import Transaction

from finance.models import DEBT_TYPES, Bill, MonzoMerchant, MonzoTransaction
from finance.utilities import DjangoHandler


class FetchTransactions:
    """Class to handle automating fetching transactions."""

    __slots__ = (
        "_account_id",
        "_auth",
        "_handler",
        "_last_transaction",
        "_process_transactions",
        "_processed_transaction_count",
        "_transaction_count",
    )

    def __init__(self):
        """Initialise MonzoAutomation."""
        self._handler: DjangoHandler = DjangoHandler()
        self._last_transaction = None
        self._process_transactions: bool = True
        self._processed_transaction_count = 0
        self._transaction_count = 0
        credentials: dict[str, Union[int, str]] = self._handler.fetch()
        self._auth = Authentication(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            redirect_url="",
            access_token=credentials["access_token"],
            access_token_expiry=credentials["expiry"],
            refresh_token=credentials["refresh_token"],
        )
        self._auth.register_callback_handler(self._handler)

    def process(self) -> dict[str, int]:
        """Process transactions."""
        self._fetch_account()
        self._fetch_transactions()
        return self._process_output()

    def _fetch_account(self):
        """Identify the correct account."""
        accounts = Account.fetch(auth=self._auth)
        for account in accounts:
            if account.account_type() == "Current Account":
                self._account_id = account.account_id
                break

    def _fetch_transactions(self):
        """Fetch transactions from Monzo."""
        since = self._handler.last_transaction_datetime
        if not since:
            self._process_transactions = False
            since = datetime.now() - timedelta(days=89)

        transactions = Transaction.fetch(
            auth=self._auth,
            account_id=self._account_id,
            since=since,
            expand=["merchant"],
        )

        if not transactions:
            return

        for tran in transactions:
            monzo_transaction = MonzoTransaction()
            monzo_transaction.transaction_id = tran.transaction_id
            monzo_transaction.currency = tran.currency
            monzo_transaction.value = tran.amount
            monzo_transaction.created = tran.created
            monzo_transaction.description = tran.description
            monzo_transaction.has_receipt = False
            if tran.merchant:
                merchant = MonzoMerchant.objects.filter(
                    merchant_id__exact=tran.description
                )
                if len(merchant):
                    monzo_transaction.merchant = merchant[0]
                else:
                    new_merchant = MonzoMerchant()
                    new_merchant.merchant_id = tran.merchant["id"]
                    new_merchant.name = tran.merchant["name"]
                    new_merchant.save()
                    monzo_transaction.merchant = new_merchant
            else:
                merchant = MonzoMerchant.objects.filter(
                    merchant_id__exact=tran.description
                )
                if len(merchant):
                    monzo_transaction.merchant = merchant[0]
                else:
                    new_merchant = MonzoMerchant()
                    new_merchant.merchant_id = tran.description
                    new_merchant.name = tran.description
                    new_merchant.save()
                    monzo_transaction.merchant = new_merchant
            monzo_transaction.save()
            if self._process_transactions:
                self._process_transaction(transaction=monzo_transaction)

            if (
                not self._last_transaction
                or monzo_transaction.created > self._last_transaction
            ):
                self._last_transaction = monzo_transaction.created
            self._transaction_count += 1

        self._handler.last_transaction_datetime = self._last_transaction

    def _process_output(self) -> dict[str, int]:
        """
        Process the output.

        Returns:
            Dict describing the output
        """
        return {
            "processed_transactions": self._processed_transaction_count,
            "transactions": self._transaction_count,
        }

    def _process_transaction(self, transaction: MonzoTransaction) -> None:
        """
        Process a given transaction to update bills.

        Args:
            transaction: Monzo transaction to process
        """
        merchant: MonzoMerchant = MonzoMerchant(transaction.merchant)
        if not merchant.for_bill:
            return
        bill: Bill = Bill(merchant.for_bill)
        if bill.bill_type in DEBT_TYPES:
            self._processed_transaction_count += 1
            bill.current_balance += transaction.value


class ProcessInterest:
    """Class to handle Adding interest."""

    def process(self) -> dict[str, int]:
        """Process transactions."""
        bills = Bill.objects.all()
        for bill in bills:
            if bill.current_balance <= 0 or bill.apr <= 0:
                continue
            self._add_interest(bill)
        return {}

    def _add_interest(self, bill: Bill):
        """
        Add interest to the given bill.

        Args:
            bill: Bill to add interest too
        """
        interest: float = self._calculate_interest(
            balance=bill.current_balance, apr=bill.apr
        )
        bill.current_balance += interest
        bill.save()

    @staticmethod
    def _calculate_interest(balance: float, apr: float) -> float:
        """
        Calculate the value of interest given the balance and APR.

        Args:
            balance: The balance of the bill
            apr: Percentage to calculate

        Returns:
            Amount of interest as a float rounded to two decimal places
        """
        monthly_apr: float = (apr / 12) / 100
        monthly_interest = balance * monthly_apr

        return round(monthly_interest, 2)
