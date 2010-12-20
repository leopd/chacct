from django.contrib import admin

import records.models as m

class FractionInline(admin.TabularInline):
    model = m.AccountFraction
    extra = 1


class TransactionTypeAdmin(admin.ModelAdmin):
    inlines = [FractionInline]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date','amount','type','comment']
    date_hierarchy = 'date'
    ordering = ['date']
    list_filter = ['type', 'date']
    
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['account', 'date', 'amount', 'is_verified']
    ordering = ['date', 'account']
    list_filter = ['account', 'date']
    date_hierarchy = 'date'
    
    
admin.site.register(m.TransactionType, TransactionTypeAdmin)
admin.site.register(m.Transaction, TransactionAdmin)
admin.site.register(m.Balance, BalanceAdmin)
admin.site.register(m.Account)
