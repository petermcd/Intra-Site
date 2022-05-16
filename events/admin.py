"""Admin configuration for the Settings application."""
from django.contrib import admin

from events.models import (
    Accommodation,
    Event,
    Hotel,
    Station,
    Travel,
    TravelType,
    Venue,
)


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "check_in",
        "for_event",
        "hotel",
    )
    ordering = ("check_in",)
    date_hierarchy = "check_in"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "description",
        "venue",
        "start",
    )
    ordering = ("name",)
    search_fields = (
        "description",
        "name",
    )
    date_hierarchy = "start"


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "city",
        "country",
    )
    ordering = ("name",)
    search_fields = (
        "name",
        "city",
        "country",
    )


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "city",
        "country",
    )
    ordering = ("name",)
    search_fields = (
        "name",
        "city",
        "country",
    )


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "departing_station",
        "arrival_station",
        "departure",
        "arrival",
    )
    ordering = ("departure",)
    date_hierarchy = "departure"


@admin.register(TravelType)
class TravelTypeAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "city",
        "country",
    )
    ordering = ("name",)
    search_fields = (
        "name",
        "city",
        "country",
    )
