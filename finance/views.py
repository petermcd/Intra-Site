from typing import Dict, Union

from django.utils.timezone import now
from django.views import generic
from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError
from monzo.handlers.storage import Storage

from finance.models import (Bill, BillAudit, Loan, LoanAudit, Monzo,
                            format_money)


def order_objects(bill_object) -> int:
    return bill_object.due_day


class BillDetailView(generic.DetailView):
    model = Bill
    template_name = 'finance/bill_details.html'

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context['recent_payments'] = BillAudit.objects.filter(for_bill=context['bill']).order_by('-when')[:15]
        return context

    def get_queryset(self):
        """
        Get event objects to display in detail view.

        Return:
            List of event objects
        """
        return Bill.objects.all()


class IndexView(generic.ListView):
    template_name = 'finance/index.html'
    context_object_name = 'bills_list'

    def get_queryset(self):
        """
        Get event objects to display in index view.

        Return:
            List of event objects
        """
        bills = Bill.objects.all().order_by('due_day')
        items = list(bills)
        loans = Loan.objects.all().filter(start_date__lt=now()).order_by('due_day')
        for loan in loans:
            items.append(loan)
        return sorted(items, key=order_objects)

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        monthly_total = 0
        to_pay = 0
        for item in context['object_list']:
            monthly_total += item.monthly_payments
            if item.last_payment and now().month != item.last_payment.month:
                to_pay += item.monthly_payments
        context['monthly_total'] = format_money(monthly_total)
        context['to_pay'] = format_money(to_pay)
        return context


class LoanDetailView(generic.DetailView):
    model = Loan
    template_name = 'finance/loan_details.html'

    def get_context_data(self, **kwargs):
        """
        Obtain context data ready for output.

        Return:
            Context data ready for output in a template
        """
        context = super().get_context_data(**kwargs)
        context['recent_payments'] = LoanAudit.objects.filter(for_loan=context['loan']).order_by('-when')[:15]
        return context

    def get_queryset(self):
        """
        Get event objects to display in detail view.

        Return:
            List of event objects
        """
        return Loan.objects.all()


class MonzoStorage(Storage):
    """
    Class to implement the Monzo API Storage handler
    """
    def store(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        expiry: int,
        refresh_token: str = ''
    ) -> None:
        """
        Store the API tokens in the Django model.

        Args:
            access_token: New access token
            client_id: Monzo client ID
            client_secret: Monzo client secret
            expiry: Access token expiry as a unix timestamp
            refresh_token: Refresh token that can be used to renew an access token
        """
        monzo_record = Monzo.objects.all()[0]
        monzo_record.access_token = access_token
        monzo_record.client_id = client_id
        monzo_record.client_secret = client_secret
        monzo_record.expiry = expiry
        monzo_record.refresh_token = refresh_token
        monzo_record.save()


class MonzoAuthView(generic.TemplateView):
    """
    Class to handle the Monzo authentication callback view.
    """
    template_name = 'admin/monzo/monzo.html'

    def get_context_data(self) -> Dict[str, Union[bool, object, str]]:
        """
        Prepare the context view to output.

        Return:
            Authentication result
        """
        return self._validate_monzo()

    def _validate_monzo(self) -> Dict[str, Union[bool, object, str]]:
        """
        Validate and process the authentication request.

        Return:
            Authentication result
        """
        monzo_record = Monzo.objects.all()
        if not monzo_record:
            context = {'success': False, 'error': 'Monzo is not configured'}
            return context
        monzo_auth = Authentication(
            client_id=monzo_record[0].client_id,
            client_secret=monzo_record[0].client_secret,
            redirect_url=monzo_record[0].redirect_url,
            access_token=monzo_record[0].access_token,
            )
        handler = MonzoStorage()
        monzo_auth.register_callback_handler(handler)
        authorization_token = self.request.GET['code']
        state_token = self.request.GET['state']
        try:
            monzo_auth.authenticate(authorization_token=authorization_token, state_token=state_token)
            context = {'success': True, 'message': 'Remember to check your phone for alerts'}
        except MonzoAuthenticationError as exc:
            context = {'success': False, 'error': exc}

        return context
