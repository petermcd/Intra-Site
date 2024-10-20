"""Views for the Finance application."""
from datetime import datetime, timedelta
from typing import Any, Union

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.views.decorators.http import require_GET, require_POST
from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError, MonzoServerError

from finance.automation import FetchTransactions, ProcessInterest
from finance.models import (
    Bill,
    BillHistory,
    Investments,
    InvestmentValue,
    MonzoMerchant,
    MonzoTransaction,
    Organisation,
)
from finance.utilities import DjangoHandler, create_redirect_url


class FinanceView(generic.ListView):
    """View to see a list of Investments."""

    template_name = "finance/bills.html"
    context_object_name = "bill_list"

    def get_queryset(self):
        """
        Get investment objects to display in index view.

        Return:
            List of Investment objects
        """
        investments = Investments.objects.all().order_by("organisation__name")
        return list(investments)


@require_GET
def bill_history(
    request, pk: int, period: str = "year"
) -> Union[HttpResponse, JsonResponse]:
    """
    View to handle fetching bill history data.

    Args:
        request: Request object
        pk: primary key for the bill to fetch data for
        period: period to fetch data for
    Returns:
        Json containing data for the given investment and period
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    response_list: list[dict[str, Union[str]]] = []
    days = 0
    weeks = 0
    if period == "day":
        days = 1
    elif period == "week":
        weeks = 1
    elif period == "month":
        days = 30
    elif period == "year":
        days = 365
    else:
        days = 1826
    time_delta = timedelta(days=days, weeks=weeks)
    lookup_time = datetime.now() - time_delta
    bill_values = BillHistory.objects.filter(date__gt=lookup_time, bill=pk).order_by(
        "date"
    )
    if len(bill_values) > 0:
        response_list.extend(
            {
                "date": bill_value.date.strftime("%Y-%m-%d"),
                "value": bill_value.current_balance,
            }
            for bill_value in bill_values
        )
    response = {
        "status": "success",
        "record_count": len(response_list),
        "data": response_list,
    }
    return JsonResponse(data=response, safe=False)


class InvestmentsView(generic.ListView):
    """View to see a list of Investments."""

    template_name = "finance/investments.html"
    context_object_name = "investment_list"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context["total"] = sum(
            investment_item.current_value
            for investment_item in context["investment_list"]
        )

        return context

    def get_queryset(self):
        """
        Get investment objects to display in index view.

        Return:
            List of Investment objects
        """
        investments = Investments.objects.all().order_by("organisation__name")
        return list(investments)


@require_GET
def investment_history(
    request, pk: int, period: str = "year"
) -> Union[HttpResponse, JsonResponse]:
    """
    View to handle fetching investment history data.

    Args:
        request: Request object
        pk: primary key for the investment to fetch data for
        period: period to fetch data for
    Returns:
        Json containing data for the given investment and period
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    response_list: list[dict[str, Union[str]]] = []
    days = 0
    weeks = 0
    if period == "day":
        days = 1
    elif period == "week":
        weeks = 1
    elif period == "month":
        days = 30
    elif period == "year":
        days = 365
    else:
        days = 1826
    time_delta = timedelta(days=days, weeks=weeks)
    lookup_time = datetime.now() - time_delta
    investment_values = InvestmentValue.objects.filter(
        date__gt=lookup_time, investment=pk
    ).order_by("date")
    if len(investment_values) > 0:
        response_list.extend(
            {
                "date": investment_value.date.strftime("%Y-%m-%d"),
                "value": investment_value.value,
            }
            for investment_value in investment_values
        )
    response = {
        "status": "success",
        "record_count": len(response_list),
        "data": response_list,
    }
    return JsonResponse(data=response, safe=False)


class Monzo(generic.TemplateView):
    """Template view to handle Monzo setup."""

    template_name = "finance/monzo.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Handle GET requests.

        Args:
            request: Request object

        Returns:
            Rendered request
        """
        context = {}
        if all(["code" in request.GET, "state" in request.GET]):
            code = request.GET["code"]
            state = request.GET["state"]
            handler = DjangoHandler()
            auth = Authentication(
                client_id=handler.client_id,
                client_secret=handler.client_secret,
                redirect_url=create_redirect_url(request=request),
            )
            auth.register_callback_handler(handler=handler)
            try:
                auth.authenticate(authorization_token=code, state_token=state)
                context[
                    "success_message"
                ] = "Monzo is now configured, remember to authorise in the app."
            except MonzoAuthenticationError:
                context["error"] = "Monzo authentication error"
            except MonzoServerError:
                context["error"] = "Monzo server error"
        else:
            context = {"redirect_url": create_redirect_url(request=request)}
        return render(
            request=request, template_name=self.template_name, context=context
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Process the post request.

        Return:
            Rendered view
        """
        context = {"redirect_url": create_redirect_url(request=request)}
        if all(["client_id" in request.POST, "client_secret" in request.POST]):
            client_id = request.POST["client_id"]
            client_secret = request.POST["client_secret"]
            handler = DjangoHandler()
            auth = Authentication(
                client_id=client_id,
                client_secret=client_secret,
                redirect_url=create_redirect_url(request=request),
            )
            handler.set_client_details(client_id=client_id, client_secret=client_secret)
            return redirect(auth.authentication_url, permanent=False)
        else:
            context["error"] = "please complete both Client ID and Client Secret"

        return render(
            request=request, template_name=self.template_name, context=context
        )


class MonzoAutomationFetchTransactionsView(generic.TemplateView):
    """View to trigger Monzo automation to fetch transactions."""

    template_name = "finance/monzo_automation.html"

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle standard get request for the Monzo automation.

        Args:
            request: Request object

        Returns:
            JSON Response
        """
        automation = FetchTransactions()

        return JsonResponse(automation.process())


class MonzoAutomationProcessInterestView(generic.TemplateView):
    """View to trigger Monzo automation to process interest."""

    template_name = "finance/monzo_automation.html"

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle standard get request for the Monzo automation.

        Args:
            request: Request object

        Returns:
            JSON Response
        """
        automation = ProcessInterest()

        return JsonResponse(automation.process())


class MonzoTransactionsView(generic.TemplateView):
    """View to trigger Monzo automation."""

    template_name = "finance/monzo_transactions.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Handle standard get request for the Monzo transactions.

        Args:
            request: Request object

        Returns:
            Rendered request
        """
        last_30_days = datetime.now() - timedelta(days=30)
        transactions = (
            MonzoTransaction.objects.all()
            .filter(created__gt=last_30_days)
            .order_by("-created")
        )
        bills = Bill.objects.all().order_by("name")

        context = {"transaction_list": transactions, "bills": bills}
        return render(
            request=request, template_name=self.template_name, context=context
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Process the post request.

        Return:
            Rendered view
        """
        linked_bill = Bill.objects.get(pk=request.POST["bill"])
        merchant = MonzoMerchant.objects.get(pk=request.POST["merchant"])
        merchant.for_bill = linked_bill
        merchant.save()
        context = {"output": linked_bill.name}
        return render(
            request=request, template_name="printed_output.html", context=context
        )


class MonzoTransactionView(generic.TemplateView):
    """View to trigger Monzo automation."""

    template_name = "finance/monzo_transaction.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Handle standard get request for a Monzo transaction.

        Args:
            request: Request object

        Returns:
            Rendered request
        """
        merchant_id = kwargs["merchant_id"]
        transactions = MonzoTransaction.objects.filter(
            merchant_id__exact=merchant_id
        ).order_by("-created")

        context = {"transaction_list": transactions, "merchant_id": merchant_id}
        return render(
            request=request, template_name=self.template_name, context=context
        )


class PaymentsView(generic.ListView):
    """View to see a list of Bills."""

    template_name = "finance/bills.html"
    context_object_name = "payment_list"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context["monthly_total"] = sum(
            payment.monthly_payments for payment in context["payment_list"]
        )
        context["from_pot_total"] = sum(
            bill_item.monthly_payments
            for bill_item in context["payment_list"]
            if bill_item.paid_from.name == "Pot"
        )
        context["from_balance_total"] = sum(
            bill_item.monthly_payments
            for bill_item in context["payment_list"]
            if bill_item.paid_from.name == "Main Balance"
        )

        return context

    def get_queryset(self):
        """
        Get investment objects to display in index view.

        Return:
            List of Investment objects
        """
        current_payments = []
        payments = Bill.objects.all().order_by("due_day")
        current_year = datetime.now().year
        current_month = datetime.now().month
        for payment in payments:
            payment_start_year = 1901
            payment_start_month = 1
            if payment.start_date:
                payment_start_year = payment.start_date.year
                payment_start_month = payment.start_date.month
            if (
                payment_start_year > current_year
                or payment_start_year == current_year
                and payment_start_month > current_month
            ):
                continue
            if payment.last_payment:
                payment_end_year = payment.last_payment.year
                payment_end_month = payment.last_payment.month
                if (
                    current_year > payment_end_year
                    or current_year == payment_end_year
                    and current_month > payment_end_month
                ):
                    continue
            current_payments.append(payment)
        return current_payments


@require_GET
def bill(request, pk: int) -> HttpResponse:
    """
    View to handle fetching data for a bill.

    Args:
        request: Request object
        pk: primary key for the bill to fetch data for

    Returns:
        HTTPResponse containing the required data
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    try:
        bill_item = Bill.objects.get(pk=pk)
    except Investments.DoesNotExist:
        return HttpResponseNotFound("No such bill")
    data = {
        "pk": bill_item.pk,
        "name": bill_item.name,
        "value": bill_item.current_balance,
    }
    return render(request, "finance/bill.html", data)


@require_GET
def bill_delete(request, pk: int) -> HttpResponse:
    """
    View to handle deleting a bill.

    Args:
        request: Request object
        pk: primary key for the bill to delete

    Returns:
        Empty response with a 200 code
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    bill_item = Bill.objects.filter(pk=pk)
    if len(bill_item) == 1:
        bill_item.delete()
    return HttpResponse(status=200)


@require_GET
def investment(request, pk: int) -> HttpResponse:
    """
    View to handle fetching data for an investment.

    Args:
        request: Request object
        pk: primary key for the investment to fetch data for

    Returns:
        HTTPResponse containing the required data
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    try:
        investment_item = Investments.objects.get(pk=pk)
    except Investments.DoesNotExist:
        return HttpResponseNotFound("No such investment")
    data = {
        "pk": investment_item.pk,
        "name": investment_item.organisation.name,
        "value": investment_item.current_value,
    }
    return render(request, "finance/investment.html", data)


@require_GET
def investment_delete(request, pk: int) -> HttpResponse:
    """
    View to handle deleting an investment.

    Args:
        request: Request object
        pk: primary key for the investment to delete

    Returns:
        Empty response with a 200 code
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    investment_item = Investments.objects.filter(pk=pk)
    if len(investment_item) == 1:
        investment_item.delete()
    return HttpResponse(status=200)


@require_POST
def investment_add(request) -> HttpResponse:
    """
    Handle adding a new investment.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    print(request.POST["invested_on"])
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    organisation = Organisation.objects.get(pk=request.POST["organisation"])
    investment_item = Investments()
    investment_item.organisation = organisation
    investment_item.description = request.POST["description"]
    investment_item.current_value = request.POST["value"]
    investment_item.date_purchased = datetime.strptime(
        request.POST["invested_on"], "%Y-%m-%d"
    )
    investment_item.save()
    context = {"investment": investment_item}
    return render(request, "finance/partials/investment_item.html", context)


@require_GET
def investment_output_form(request) -> HttpResponse:
    """
    Handle outputting the form for adding a new task item.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    context = {"organisations": Organisation.objects.all().order_by("name")}
    return render(request, "finance/partials/investment_add_form.html", context)
