from django.contrib import admin

from events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starting', 'ending',)
    ordering = ('starting',)


admin.site.register(Event, EventAdmin)
