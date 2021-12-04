from django.contrib import admin

from network.models import (IP, Device, DeviceManufacturer, DeviceModel,
                            DeviceType, Domains, OperatingSystemVendor,
                            OperatingSystemVersion, Registrar, Subdomain,
                            Website)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('hostname', 'ip', 'device_type', 'model')
    ordering = ('hostname',)


@admin.register(DeviceManufacturer)
class DeviceManufacturerAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('manufacturer', 'model',)
    ordering = ('manufacturer', 'model',)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Domains)
class DomainsAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'registrar',)
    ordering = ('name',)


@admin.register(IP)
class IPAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('address',)
    ordering = ('address',)


@admin.register(OperatingSystemVendor)
class OperatingSystemVendorAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(OperatingSystemVersion)
class OperatingSystemVersionAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('vendor', 'version',)
    ordering = ('vendor', 'version',)


@admin.register(Registrar)
class RegistrarAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('subdomain', 'domain', 'device',)
    ordering = ('domain', 'subdomain',)


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'full_url',)
    ordering = ('name',)
