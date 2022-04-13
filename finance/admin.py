"""Admin configuration for the Finance application."""
from django.contrib import admin

from finance.models import Bill, BillType, Investments, Organisation, PaidFrom


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Admin for the Bill model."""

    list_display = (
        "name",
        "description",
        "monthly_payments",
        "current_balance",
        "apr",
        "paid_from",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("name",)
    list_per_page = 20


@admin.register(BillType)
class BillTypeAdmin(admin.ModelAdmin):
    """Admin for the BillType model."""

    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


@admin.register(Investments)
class InvestmentsAdmin(admin.ModelAdmin):
    """Admin for the Investments model."""

    list_display = (
        "organisation",
        "description",
        "current_value",
    )
    ordering = ("organisation",)
    search_fields = ("description",)
    date_hierarchy = "date_purchased"
    list_per_page = 20


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """Admin for the Organisation model."""

    list_display = (
        "name",
        "description",
        "url",
    )
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 20


@admin.register(PaidFrom)
class PaidFromAdmin(admin.ModelAdmin):
    """Admin for the PaidFrom model."""

    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20
