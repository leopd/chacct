import sys
import re
import logging
import datetime
import csv
from django.core.management.base import BaseCommand, CommandError

import records.models as m

class Command(BaseCommand):
    args = 'filename.csv'
    help = 'Loads transactions in CSV format: Date (mm/dd/yyyy), Comment, Amount, Transaction type'


    def parse_bucks(self,s):
        no_commas = re.sub(',','',s)
        no_commas = re.sub('\\$','',no_commas)
        if no_commas[0] == '(' and no_commas[-1]==')':
            no_commas= no_commas[1:-1]
        return float(no_commas)
        

    def handle(self, *args, **options):
        filename = args[0]
        fh = open(filename,'r')
        csv_reader = csv.reader(fh)
        new_transactions = []
        for row in csv_reader:
            date = datetime.datetime.strptime(row[0],'%m/%d/%Y').date()
            comment = row[1]
            amount = self.parse_bucks(row[2])
            typename = row[3]

            try:
                ttype = m.TransactionType.objects.get(name=typename)
            except m.TransactionType.DoesNotExist:
                print "No transaction type matching name='%s'" % typename
                print "Aborting import"
                sys.exit(-1)
            trans = m.Transaction(amount = amount,
                                  date = date,
                                  comment = comment,
                                  type = ttype,
                                  )
            new_transactions.append(trans)

        print "Saving %s new transactions" % len(new_transactions)
        for trans in new_transactions:
            trans.save()
        print "Done."

