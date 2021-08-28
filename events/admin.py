from django.contrib import admin

from events.models import Event, Venue


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting', 'ending',)
    ordering = ('starting',)


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'town', 'country',)
    ordering = ('name',)


admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
