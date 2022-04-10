"""Views for the Finance application."""
from datetime import datetime, timedelta
from typing import Union

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import generic

from finance.models import Investments, InvestmentValue


class FinanceView(generic.ListView):
    """View to see a list of Investments."""

    template_name = "finance/finance_index.html"
    context_object_name = "investment_list"

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

    def get_queryset(self):
        """
        Get investment objects to display in index view.

        Return:
            List of Investment objects
        """
        investments = Investments.objects.all().order_by("organisation__name")
        return list(investments)


class PaymentsView(generic.ListView):
    """View to see a list of Investments."""

    template_name = "finance/finance_index.html"
    context_object_name = "investment_list"

    def get_queryset(self):
        """
        Get investment objects to display in index view.

        Return:
            List of Investment objects
        """
        investments = Investments.objects.all().order_by("organisation__name")
        return list(investments)


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
    investment = Investments.objects.filter(pk=pk)
    if len(investment) == 1:
        investment.delete()
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
