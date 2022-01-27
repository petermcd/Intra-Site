from django.contrib import admin

from networkv2.models import (ConnectionType, Device, DeviceType, Domain, Manufacturer,
                              Model, OperatingSystem, Registrar, Subdomain,
                              Vendor, Website)


@admin.register(ConnectionType)
class ConnectionTypesAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'unique_port',)
    ordering = ('name',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('hostname', 'ip',)
    ordering = ('hostname',)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'image',)
    ordering = ('name',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'registrar',)
    ordering = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'manufacturer',)
    ordering = ('name',)


@admin.register(OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
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
    list_display = ('name', 'domain', 'hosted_on',)
    ordering = ('name',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """
    list_display = ('name', 'full_url', 'description',)
    ordering = ('name',)
