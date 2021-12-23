from django.contrib import admin
from django.utils.safestring import mark_safe

from finance.models import Lender, Loan, Merchant, Monzo


@admin.register(Monzo)
class FinanceAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """

    def has_add_permission(self, request):
        return True

    def add_view(self, *args, **kwargs):
        """
        Create view for configuring items.
        """
        self.exclude = ['access_token', 'expiry', 'refresh_token']
        return super(FinanceAdmin, self).add_view(*args, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Modify view so that some fields are hidden.
        """
        self.exclude = ['access_token', 'expiry', 'refresh_token']
        return super(FinanceAdmin, self).change_view(request, object_id, form_url, extra_context)

    def output_link_url(self):
        return mark_safe(self.link_url())

    list_display = ('linked', output_link_url,)


@admin.register(Lender)
class LenderAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('lender', 'due_day', 'apr', 'merchant_configured',)
    ordering = ('lender', 'due_day',)
