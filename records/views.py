import logging

import re

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

import records.models as m

def _row_from_current_balances(current_balances, date, accounts):
    balances = []
    for acct in accounts:
        m = re.match("^(.*) TOTAL",acct.name)
        if m:
            prefix = m.group(1)
            total = 0
            for a in accounts:
                if a.name.startswith(prefix):
                    total += current_balances[a]
            val = total
        else:
            val = current_balances[acct]
        balances.append( round(val,2) )
    return row
                
    
    
def dollar_format(flt, add_plus = False):
    if flt == 0:
        return 0
    str = "%.2f" % flt
    commas = re.sub("(\d)(?=(\d{3})+\.)","\g<1>,",str)
    if add_plus and flt > 0:
        commas = "+" + commas
    return commas

@login_required
def calculate_register(request):
    accts = []
    balances = {}
    for acct in m.Account.objects.all():
        accts.append(acct)
        balances[acct] = 0.0
    result = []
    
    qs = m.Transaction.objects.all().order_by('date','id')
    for transaction in qs.iterator():
        row = {'transaction': transaction, 
               'per_account_details': [], 
               }
        # First pass, apply the transactions
        deltas = {}
        for acct in accts:
            details = {}
            delta = transaction.amount_for(acct)
            balances[acct] += delta
            deltas[acct] = delta
        # Second pass, output the display and look for TOTAL
        for acct in accts:
            details = {}
            match = re.match("^(.*) TOTAL",acct.name)
            if match:
                prefix = match.group(1)
                total = 0
                delta = 0
                for a in accts:
                    if a.name.startswith(prefix):
                        total += balances[a]
                        delta += deltas[a]
                details['balance'] = total
                details['delta'] = delta
            else:
                details['balance'] = balances[acct]
                details['delta'] = deltas[acct]
            row['per_account_details'].append(details)
        result.append(row)
        logging.debug(row)
    return render_to_response("records/register2.html", {
                            'register': result,
                            'accounts': accts,
                    })
