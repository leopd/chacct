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
    
    
    
class BalanceInline(admin.TabularInline):
    model = m.Balance
    extra = 0
    max_num = 50
    fields = ['date','amount', 'is_verified']
    readonly_fields = ['date','amount']
    
    
class AccountAdmin(admin.ModelAdmin):
    actions = ['balance_accounts']
    inlines = [BalanceInline]
    
    def balance_accounts(self,request,queryset):
        num = 0
        for acct in queryset.all():
            acct.calculate_balances()
            num += 1
        
        # see http://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/
        self.message_user(request,"%s account(s) balanced" % num)
        
        
    
        
    
    
admin.site.register(m.TransactionType, TransactionTypeAdmin)
admin.site.register(m.Transaction, TransactionAdmin)
admin.site.register(m.Balance, BalanceAdmin)
admin.site.register(m.Account, AccountAdmin)
