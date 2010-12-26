
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

import records.models as m

def _row_from_current_balances(current_balances, date, accounts):
    
    balances = []
    for acct in accounts:
        val = current_balances[acct]
        balances.append( round(val,2) )
    row = {'Date': date, 'Balances': balances }
    return row
                
@login_required
def show_register(self):
    register = []
    current_balances = {}
    for acct in m.Account.objects.all():
        current_balances[acct]=0
    current_balances['Date'] = None
    last_date = None
    
    accounts = m.Account.objects.all()
    
    for balance in m.Balance.objects.all().order_by('date'):
        if balance.date != current_balances['Date']:
            # Emit a row into register
            if last_date:
                row = _row_from_current_balances(current_balances, last_date, accounts)
                register.append(row)
            last_date = balance.date
        current_balances[balance.account] = balance.amount
        
    return render_to_response("records/show_register.html", {
                            'register': register,
                            'accounts': accounts,
                    })
    
    
    
    

