from django.contrib import admin

from .models import (IP, ConnectionMethod, Device, DeviceCategory, DeviceType,
                     DNSProvider, Domain, MonitoringGroup, MonitoringTemplate,
                     Registrar, Settings, Site)


@admin.register(ConnectionMethod)
class ConnectionMethodAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'ip', 'description',)
    ordering = ('name',)


@admin.register(DeviceCategory)
class DeviceCategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'description', 'category',)
    ordering = ('manufacturer', 'model',)


@admin.register(DNSProvider)
class DNSProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(IP)
class IPAdmin(admin.ModelAdmin):
    ordering = ('ip',)


@admin.register(MonitoringGroup)
class MonitoringGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_id',)
    ordering = ('name',)


@admin.register(MonitoringTemplate)
class MonitoringTemplateAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'template_id',)


@admin.register(Registrar)
class RegistrarAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value',)
    ordering = ('name',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
