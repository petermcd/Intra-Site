import datetime

from django.views import generic

from .models import Debt, Payments, format_money


class IndexView(generic.ListView):
    template_name = 'finance/index.html'
    context_object_name = 'finance_payments_list'

    def get_queryset(self):
        return Payments().monthly_payments()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['paid'], data['to_pay'], data['total'] = self._calculate_totals(self.get_queryset())
        return data

    @staticmethod
    def _calculate_totals(payments):
        current_day = datetime.date.today().day
        paid = 0
        to_pay = 0
        for payment in payments:
            if payment.payment_day > current_day:
                to_pay += payment.payment_amount
            else:
                paid += payment.payment_amount

        total = format_money(to_pay + paid)
        paid = format_money(paid)
        to_pay = format_money(to_pay)
        return paid, to_pay, total


class DetailView(generic.DetailView):
    model = Debt
    template_name = 'finance/detail.html'

    def get_queryset(self):
        return Debt.objects.all()