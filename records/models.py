import datetime
import logging
from django.db import models

class Account(models.Model):
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    class Meta:
        ordering = ['name']
    
    def calculate_balances(self):
        """Creates all the appropriate balance objects on this account
        by inspecting the transaction objects that refer to it.
        """
        logging.info("Calculating balances for %s" % self)
        self._clear_all_balances()
        
        qs = Transaction.objects.filter(type__debitcredit = self).order_by('date')
        running_balance = 0.00
        for transaction in qs.iterator():
            delta = transaction.amount_for(self)
            running_balance += delta
            logging.debug("Applying transaction %s. Balance is %s" % (transaction, running_balance))
            b = Balance(account = self,
                        amount = running_balance,
                        date = transaction.date,
                        calculated_on = datetime.datetime.now(),
                        )
            b.save()
        logging.debug("Done with balances for %s" % self)
    
    def _clear_all_balances(self):
        for b in self.balance_set.all():
            b.delete()


class TransactionType(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    debitcredit = models.ManyToManyField(Account, through='AccountFraction')
    valid_from = models.DateField(null = True, blank = True)
    valid_until = models.DateField(null = True, blank = True)
                                        
    def __unicode__(self):
        return u"%s" % self.name
    
    class Meta:
        ordering = ['name']
        
    def fraction_for(self, account):
        try:
            fraction_obj = AccountFraction.objects.get(transactiontype = self, account = account)
            return fraction_obj.fraction
        except AccountFraction.DoesNotExist:
            return 0.0
    
    
class AccountFraction(models.Model):
    transactiontype = models.ForeignKey(TransactionType)
    account = models.ForeignKey(Account)
    fraction = models.FloatField()
    
    def __unicode__(self):
        return u"%s at %.2f%%" % (self.account, self.fraction*100)
    
    
class Transaction(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    comment = models.CharField(null = True, blank = True, max_length=200)
    type = models.ForeignKey(TransactionType)
    
    def __unicode__(self):
        return u"%s | $%.2f | %s" % (self.date, self.amount, self.type)
    
    def amount_for(self, account):
        """Figures out the amount of this transaction that applies
        to the specified account.
        """
        fraction = self.type.fraction_for(account)
        return self.amount * fraction
    
    
class Balance(models.Model):
    account = models.ForeignKey(Account)
    date = models.DateField()
    amount = models.FloatField()
    calculated_on = models.DateTimeField(null = True, blank = True)
    is_verified = models.BooleanField(default = False)
    verified_on = models.DateTimeField(null = True, blank = True)
    
    
        
