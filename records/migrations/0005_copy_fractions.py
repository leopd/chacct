# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for tt in orm.TransactionType.objects.all():
            td = orm.TransactionDistribution(type = tt)
            td.save()
            for frac in tt.accountfraction_set.all():
                frac2 = orm.AccountFraction2(distribution = td,
                                             account = frac.account,
                                             fraction = frac.fraction,
                                             )
                frac2.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("No backwards migration.  I'm lazy.")


    models = {
        'records.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'records.accountfraction': {
            'Meta': {'object_name': 'AccountFraction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.Account']"}),
            'fraction': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transactiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.TransactionType']"})
        },
        'records.accountfraction2': {
            'Meta': {'object_name': 'AccountFraction2'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.Account']"}),
            'distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.TransactionDistribution']"}),
            'fraction': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'records.balance': {
            'Meta': {'object_name': 'Balance'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'calculated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'records.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.TransactionType']"})
        },
        'records.transactiondistribution': {
            'Meta': {'object_name': 'TransactionDistribution'},
            'debitcredit': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['records.Account']", 'through': "orm['records.AccountFraction2']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['records.TransactionType']"}),
            'valid_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'records.transactiontype': {
            'Meta': {'ordering': "['name']", 'object_name': 'TransactionType'},
            'debitcredit': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['records.Account']", 'through': "orm['records.AccountFraction']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['records']
