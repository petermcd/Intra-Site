from django.contrib import admin

from .models import Bill, Company, Debt, Investment


class BillAdmin(admin.ModelAdmin):
    list_display = ('company', 'payment_amount_clean', 'payment_day',)
    ordering = ('company',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    ordering = ('name',)


class DebtAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_amount_clean', 'current_balance_clean', 'remaining_payment_count',)
    ordering = ('company',)


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'value',)
    ordering = ('company', 'name',)


admin.site.register(Bill, BillAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Debt, DebtAdmin)
admin.site.register(Investment, InvestmentAdmin)
