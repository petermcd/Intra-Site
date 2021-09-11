from django.contrib import admin

from .models import Bill, Company, Debt, Investment


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('company', 'payment_amount_clean', 'payment_day',)
    ordering = ('company',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_amount_clean', 'current_balance_clean', 'remaining_payment_count',)
    ordering = ('company',)


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'value_clean',)
    ordering = ('name', 'company',)
