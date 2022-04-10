"""Admin configuration for the Finance application."""
from django.contrib import admin

from finance.models import Investments, Organisation


@admin.register(Investments)
class InvestmentsAdmin(admin.ModelAdmin):
    """Admin for the Investments model."""

    list_display = (
        "organisation",
        "description",
        "current_value",
    )
    search_fields = ("description",)
    ordering = ("organisation",)
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
