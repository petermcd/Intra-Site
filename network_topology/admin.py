from django.contrib import admin

from .models import (
    AnsibleGroup,
    ConnectionMethod,
    Device,
    DeviceCategory,
    DeviceType,
    IP,
    MonitoringTemplate,
    Settings,
    Site
)


class AnsibleGroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)


class ConnectionMethodAdmin(admin.ModelAdmin):
    ordering = ('name',)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'ip', 'description')
    ordering = ('name',)


class DeviceCategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'description', 'category')
    ordering = ('manufacturer', 'model')


class IPAdmin(admin.ModelAdmin):
    ordering = ('ip',)


class MonitoringTemplateAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'template_id')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    ordering = ('name',)

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    ordering = ('name',)


admin.site.register(Settings, SettingsAdmin)
admin.site.register(AnsibleGroup, AnsibleGroupsAdmin)
admin.site.register(ConnectionMethod, ConnectionMethodAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceCategory, DeviceCategoryAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(MonitoringTemplate, MonitoringTemplateAdmin)
admin.site.register(Site, SiteAdmin)
