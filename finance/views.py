from django.shortcuts import render
from django.views import generic

from .models import Debt, Bill, Payments


class IndexView(generic.ListView):
    template_name = 'finance/index.html'
    context_object_name = 'finance_payments_list'

    def get_queryset(self):
        return Payments().monthly_payments()


class DetailView(generic.DetailView):
    model = Debt
    template_name = 'finance/detail.html'

    def get_queryset(self):
        return Debt.objects.all()