# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('records_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('records', ['Account'])

        # Adding model 'TransactionType'
        db.create_table('records_transactiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('valid_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('valid_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('records', ['TransactionType'])

        # Adding model 'AccountFraction'
        db.create_table('records_accountfraction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transactiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['records.TransactionType'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['records.Account'])),
            ('fraction', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('records', ['AccountFraction'])

        # Adding model 'Transaction'
        db.create_table('records_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['records.TransactionType'])),
        ))
        db.send_create_signal('records', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('records_account')

        # Deleting model 'TransactionType'
        db.delete_table('records_transactiontype')

        # Deleting model 'AccountFraction'
        db.delete_table('records_accountfraction')

        # Deleting model 'Transaction'
        db.delete_table('records_transaction')


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
