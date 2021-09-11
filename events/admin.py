from django.contrib import admin

from events.models import Event, EventTravel, TransportMethod, Venue


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting', 'ending', 'travel_arranged',)
    ordering = ('starting',)


@admin.register(EventTravel)
class EventTravelAdmin(admin.ModelAdmin):
    list_display = ('method', 'venue_name', 'event_name', 'starting',)
    ordering = ('starting',)


@admin.register(TransportMethod)
class TransportMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'town', 'country',)
    ordering = ('name',)
