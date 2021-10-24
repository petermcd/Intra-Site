from django.contrib import admin

from events.models import Event, Station, Travel, Venue


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'description', 'venue', 'start',)
    ordering = ('name',)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'city', 'country',)
    ordering = ('name',)


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('departing_station', 'arrival_station', 'departure', 'arrival',)
    ordering = ('departure',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'city', 'country',)
    ordering = ('name',)
