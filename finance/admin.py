from django.contrib import admin

from .models import Bill, Company, Debt


class BillAdmin(admin.ModelAdmin):
    list_display = ('company', 'payment_amount_clean', 'payment_day')
    ordering = ('company',)


class DebtAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_amount_clean', 'current_balance_clean', 'remaining_payment_count')
    ordering = ('company',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    ordering = ('name',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Debt, DebtAdmin)
