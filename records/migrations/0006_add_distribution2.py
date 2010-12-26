# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'AccountFraction'
        db.delete_table('records_accountfraction')


    def backwards(self, orm):
        
        # Adding model 'AccountFraction'
        db.create_table('records_accountfraction', (
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['records.Account'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fraction', self.gf('django.db.models.fields.FloatField')()),
            ('transactiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['records.TransactionType'])),
        ))
        db.send_create_signal('records', ['AccountFraction'])


    models = {
        'records.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['records']
