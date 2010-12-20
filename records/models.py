from django.db import models

class Account(models.Model):
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return u"%s" % self.name
    

class TransactionType(models.Model):
    name = models.CharField(max_length = 100)
    debitcredit = models.ManyToManyField(Account, through='AccountFraction')
    valid_from = models.DateField(null = True, blank = True)
    valid_until = models.DateField(null = True, blank = True)
                                        
    def __unicode__(self):
        return u"%s" % self.name
    
    
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
    
