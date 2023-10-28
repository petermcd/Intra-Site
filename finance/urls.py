"""URL configuration for the Finance application."""
from django.urls import path

from finance.views import (
    FinanceView,
    InvestmentsView,
    Monzo,
    MonzoAutomationFetchTransactionsView,
    MonzoAutomationProcessInterestView,
    MonzoTransactionsView,
    MonzoTransactionView,
    PaymentsView,
    bill,
    bill_delete,
    bill_history,
    investment,
    investment_add,
    investment_delete,
    investment_history,
    investment_output_form,
)

app_name = "finance"
urlpatterns = [
    path("", FinanceView.as_view(), name="finance_index"),
    path("investments/", InvestmentsView.as_view(), name="investments"),
    path("investments/form", investment_output_form, name="investment_output_form"),
    path("investments/add", investment_add, name="investment_add"),
    path("investments/<int:pk>/", investment, name="investment"),
    path("investments/<int:pk>/delete", investment_delete, name="investments_delete"),
    path(
        "investments/<int:pk>/<str:period>.json",
        investment_history,
        name="investments_json",
    ),
    path("monzo/", Monzo.as_view(), name="configure_monzo"),
    path(
        "monzo/automation/fetch_transactions",
        MonzoAutomationFetchTransactionsView.as_view(),
        name="monzo_automation",
    ),
    path(
        "monzo/automation/process_interest",
        MonzoAutomationProcessInterestView.as_view(),
        name="monzo_automation",
    ),
    path(
        "monzo/transactions/",
        MonzoTransactionsView.as_view(),
        name="monzo_transactions",
    ),
    path(
        "monzo/transactions/<str:merchant_id>/",
        MonzoTransactionView.as_view(),
        name="monzo_transaction",
    ),
    path("payments/", PaymentsView.as_view(), name="payments"),
    path("payments/<int:pk>/", bill, name="bill"),
    path("payments/<int:pk>/delete", bill_delete, name="bill_delete"),
    path("payments/<int:pk>/<str:period>.json", bill_history, name="bill_json"),
]
