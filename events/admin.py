from django.contrib import admin

from events.models import Event, EventTravel, TransportMethod, Venue


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting', 'ending',)
    ordering = ('starting',)


class EventTravelAdmin(admin.ModelAdmin):
    list_display = ('method', 'venue_name', 'event_name', 'starting',)
    ordering = ('starting',)


class TransportMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'town', 'country',)
    ordering = ('name',)


admin.site.register(Event, EventAdmin)
admin.site.register(EventTravel, EventTravelAdmin)
admin.site.register(TransportMethod, TransportMethodAdmin)
admin.site.register(Venue, VenueAdmin)
