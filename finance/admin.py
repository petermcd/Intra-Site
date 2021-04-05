from django.contrib import admin

from .models import Bill, Company, Currency, Debt


class BillAdmin(admin.ModelAdmin):
    list_display = ('company', 'payment_amount_clean')


class DebtAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_amount_clean', 'current_balance_clean', 'remaining_payment_count')


admin.site.register(Currency)
admin.site.register(Company)
admin.site.register(Bill, BillAdmin)
admin.site.register(Debt, DebtAdmin)
