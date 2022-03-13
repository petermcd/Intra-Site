from django.contrib import admin

from settings.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """
    Configure the admin page.
    """

    list_display = (
        "name",
        "description",
        "configured",
    )
    ordering = ("name",)
