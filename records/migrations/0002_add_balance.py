# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Balance'
        db.create_table('records_balance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['records.Account'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('calculated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('records', ['Balance'])


    def backwards(self, orm):
        
        # Deleting model 'Balance'
        db.delete_table('records_balance')


    models = {
        'records.account': {
            'Meta': {'object_name': 'Account'},
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
        'records.transactiontype': {
            'Meta': {'object_name': 'TransactionType'},
            'debitcredit': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['records.Account']", 'through': "orm['records.AccountFraction']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valid_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['records']
