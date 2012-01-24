"""This defines the data structure for the system.
Each Class corresponds to a RDBMS table.

There are 6 classes:
-Account (like Mortgage, Utilities, an owner)
    -Balance (ephemeral.  Gets blown away and recreated on request.)

-Transaction (money moving on a date)
    -TransactionType (classifies why the money moved)
        -TransactionDistribution (describes how the money is distributed to accounts)
            -AccountFraction (joins Distribution to Account with a percentage)

"""
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
        
        #qs = Transaction.objects.filter(type__transactiondistribution__debitcredit = self).order_by('date')
        qs = Transaction.objects.all().order_by('date')
        running_balance = 0.00
        for transaction in qs.iterator():
            delta = transaction.amount_for(self)
            if delta != 0.0:
	            running_balance += delta
	            logging.debug("Applying transaction %s. Balance is %s" % (transaction, running_balance))
	            b = Balance(account = self,
	                        amount = running_balance,
	                        date = transaction.date,
                            ref_transaction = transaction,
	                        calculated_on = datetime.datetime.now(),
	                        )
	            b.save()
        logging.debug("Done with balances for %s" % self)
    
    def _clear_all_balances(self):
        for b in self.balance_set.all():
            b.delete()


class TransactionType(models.Model):
    name = models.CharField(max_length = 100, unique = True)
                                        
    def __unicode__(self):
        return u"%s" % self.name
    
    class Meta:
        ordering = ['name']
        
    def distribution_for(self, date):
        """Figures out which TransactionDistribution object applies on this date.
        """
        for dist in self.transactiondistribution_set.all():
            if dist.valid_from is None and dist.valid_until is None:
                return dist
            if dist.valid_from is None and date <= dist.valid_until:
                return dist
            if dist.valid_until is None and dist.valid_from <= date:
                return dist
            if dist.valid_from <= date and dist.valid_until <= date:
                return dist
        return None
        
        
    def fraction_for(self, account, date):
        """Figures out what fraction goes to this account on this date.
        """
        dist_obj = self.distribution_for(date)
        if dist_obj is None:
            logging.warning("No distribution object for %s on %s" % (self,date))
            return 0.0
        try:
            #fraction_obj = AccountFraction.objects.get(transactiontype = self, account = account)
            fraction_obj = AccountFraction.objects.get(distribution = dist_obj, account = account)
            return fraction_obj.fraction
        except AccountFraction.DoesNotExist:
            return 0.0
        
        
class TransactionDistribution(models.Model):
    """How a transaction type is distributed to accounts.
    This is time-dependent.
    """
    type = models.ForeignKey(TransactionType)
    debitcredit = models.ManyToManyField(Account, through='AccountFraction')
    valid_from = models.DateField(null = True, blank = True)
    valid_until = models.DateField(null = True, blank = True)
    
    def __unicode__(self):
        if self.valid_from or self.valid_until:
            return u"Distribution for %s (from %s to %s)" % (self.type, self.valid_from, self.valid_until) 
        else:
            return u"Distribution for %s (always)" % self.type
        
    
    def fraction_for(self, account):
        try:
            fraction_obj = AccountFraction.objects.get(transactiontype = self, account = account)
            return fraction_obj.fraction
        except AccountFraction.DoesNotExist:
            return 0.0
    
    
class AccountFraction(models.Model):
    """This is the many-many join table between Distribution and Account
    it adds percentage to the association.
    """
    distribution = models.ForeignKey(TransactionDistribution)
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
        fraction = self.type.fraction_for(account, self.date)
        return self.amount * fraction
    
    
class Balance(models.Model):
    account = models.ForeignKey(Account)
    date = models.DateField()
    amount = models.FloatField()
    ref_transaction = models.ForeignKey(Transaction, null = True, blank = True)
    calculated_on = models.DateTimeField(null = True, blank = True)
    is_verified = models.BooleanField(default = False)
    verified_on = models.DateTimeField(null = True, blank = True)
    
    
        
