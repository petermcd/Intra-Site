from django.contrib import admin
from events.models import Event

from django.utils.timezone import now


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting', 'ending',)
    ordering = ('starting',)


admin.site.register(Event, EventAdmin)
