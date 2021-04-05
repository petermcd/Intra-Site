from django.contrib import admin

from .models import IP, ConnectionMethod, Device, DeviceType

admin.site.register(ConnectionMethod)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(IP)
