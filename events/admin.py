"""Admin configuration for Events."""
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


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "city",
        "country",
    )
    ordering = ("name",)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "city",
        "country",
    )
    ordering = ("name",)


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


@admin.register(TravelType)
class TravelTypeAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = ("name",)
    ordering = ("name",)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Configure the admin page."""

    list_display = (
        "name",
        "city",
        "country",
    )
    ordering = ("name",)
