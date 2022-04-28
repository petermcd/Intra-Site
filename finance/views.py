"""Views for the Finance application."""
from datetime import datetime, timedelta
from typing import Union

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import generic

from finance.models import Bill, BillHistory, Investments, InvestmentValue, Organisation


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


class InvestmentsView(generic.ListView):
    """View to see a list of Investments."""

    template_name = "finance/investments.html"
    context_object_name = "investment_list"

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context["total"]: float = sum(
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


class PaymentsView(generic.ListView):
    """View to see a list of Bills."""

    template_name = "finance/bills.html"
    context_object_name = "payment_list"

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context["monthly_total"]: float = sum(
            payment.monthly_payments for payment in context["payment_list"]
        )
        context["from_pot_total"]: float = sum(
            bill_item.monthly_payments
            for bill_item in context["payment_list"]
            if bill_item.paid_from.name == "Pot"
        )
        context["from_balance_total"]: float = sum(
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


def bill(request, pk: int):
    """
    View to handle fetching data for a bill.

    Args:
        request: Request object
        pk: primary key for the bill to fetch data for

    Returns:
        HTTPResponse containing the required data
    """
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


def bill_history(request, pk: int, period: str = "year"):
    """
    View to handle fetching bill history data.

    Args:
        request: Request object
        pk: primary key for the bill to fetch data for
        period: period to fetch data for

    Returns:
        Json containing data for the given investment and period
    """
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


def bill_delete(request, pk: int):
    """
    View to handle deleting a bill.

    Args:
        request: Request object
        pk: primary key for the bill to delete

    Returns:
        Empty response with a 200 code
    """
    bill_item = Bill.objects.filter(pk=pk)
    if len(bill_item) == 1:
        bill_item.delete()
    return HttpResponse(status=200)


def investment(request, pk: int):
    """
    View to handle fetching data for an investment.

    Args:
        request: Request object
        pk: primary key for the investment to fetch data for

    Returns:
        HTTPResponse containing the required data
    """
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


def investment_delete(request, pk: int):
    """
    View to handle deleting an investment.

    Args:
        request: Request object
        pk: primary key for the investment to delete

    Returns:
        Empty response with a 200 code
    """
    investment_item = Investments.objects.filter(pk=pk)
    if len(investment_item) == 1:
        investment_item.delete()
    return HttpResponse(status=200)


def investment_history(request, pk: int, period: str = "year"):
    """
    View to handle fetching investment history data.

    Args:
        request: Request object
        pk: primary key for the investment to fetch data for
        period: period to fetch data for

    Returns:
        Json containing data for the given investment and period
    """
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


def investment_add(request):
    """
    Handle adding a new investment.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    organisation = Organisation.objects.get(pk=request.POST["organisation"])
    investment_item = Investments()
    investment_item.organisation = organisation
    investment_item.description = request.POST["description"]
    investment_item.current_value = request.POST["value"]
    investment_item.date_purchased = datetime.strptime(
        request.POST["invested_on"], "%d-%m-%Y %H:%M"
    )
    investment_item.save()
    context = {"investment": investment_item}
    return render(request, "finance/partials/investment_item.html", context)


def investment_output_form(request):
    """
    Handle outputting the form for adding a new task item.

    Args:
        request: Request object

    Returns:
        Rendered form
    """
    context = {"organisations": Organisation.objects.all().order_by("name")}
    return render(request, "finance/partials/investment_add_form.html", context)
