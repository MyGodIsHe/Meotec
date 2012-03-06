# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Server'
        db.create_table('base_manager_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base_manager', ['Server'])

        # Adding model 'Site'
        db.create_table('base_manager_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('repository', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base_manager', ['Site'])


    def backwards(self, orm):
        
        # Deleting model 'Server'
        db.delete_table('base_manager_server')

        # Deleting model 'Site'
        db.delete_table('base_manager_site')


    models = {
        'base_manager.server': {
            'Meta': {'object_name': 'Server'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base_manager.site': {
            'Meta': {'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repository': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['base_manager']
