from django.contrib import admin

from .models import Device, DeviceType, IP


admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(IP)
