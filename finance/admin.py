from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse

from finance.models import Monzo


@admin.register(Monzo)
class FinanceAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return True

    def get_urls(self):
        urls = super(FinanceAdmin, self).get_urls()
        monzo_urls = [
            # TODO https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#overriding-the-default-admin-site
            url('kjhgfd', self.admin_site.admin_view(self.monzo_configuration))
        ]
        print(monzo_urls + urls)
        return monzo_urls + urls

    # Your view definition fn
    def monzo_configuration(self, request):
        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, "finance/admin/monzo.html", context)

    def add_view(self, *args, **kwargs):
        self.exclude = ['access_token', 'expiry', 'refresh_token']
        return super(FinanceAdmin, self).add_view(*args, **kwargs)
