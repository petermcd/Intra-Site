"""Admin configuration for Finance."""
from django.contrib import admin
from django.utils.safestring import mark_safe

from finance.models import Bill, Investment, Lender, Loan, Monzo, PaidFrom


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "company",
        "due_day",
        "merchant_configured",
    )
    ordering = (
        "company",
        "due_day",
    )


@admin.register(Lender)
class LenderAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "url",
    )
    ordering = ("name",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "lender",
        "due_day",
        "apr",
        "merchant_configured",
    )
    ordering = (
        "lender",
        "due_day",
    )


@admin.register(Monzo)
class MonzoAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    def has_add_permission(self, request):
        """
        Identify if the user has add permissions.

        Args:
            request: The http request details

        Returns:
            True
        """
        return True

    def add_view(self, *args, **kwargs):
        """Create view for configuring items."""
        self.exclude = ["access_token", "expiry", "last_fetch", "refresh_token"]
        return super(MonzoAdmin, self).add_view(*args, **kwargs)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """
        Modify view so that some fields are hidden.

        Args:
            request: The http request details
            object_id: Object ID
            form_url: Form URL
            extra_context: Extra content

        Returns: Updated context
        """
        self.exclude = ["access_token", "expiry", "last_fetch", "refresh_token"]
        return super(MonzoAdmin, self).change_view(
            request, object_id, form_url, extra_context
        )

    def output_link_url(self) -> str:
        """
        Output the link URL.

        Returns:
            Link as a string
        """
        return mark_safe(self.link_url())

    list_display = (
        "linked",
        output_link_url,
    )


@admin.register(PaidFrom)
class PaidFromAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "company",
        "value",
    )
    ordering = ("company",)
