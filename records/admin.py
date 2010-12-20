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
    
    
admin.site.register(m.TransactionType, TransactionTypeAdmin)
admin.site.register(m.Transaction, TransactionAdmin)
admin.site.register(m.Account)
