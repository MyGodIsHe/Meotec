# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Manager'
        db.create_table('meotec_manager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('repository', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('meotec', ['Manager'])

        # Adding model 'Command'
        db.create_table('meotec_command', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('args', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('meotec', ['Command'])

        # Adding model 'Server'
        db.create_table('meotec_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('meotec', ['Server'])

        # Adding model 'Site'
        db.create_table('meotec_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('repository', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meotec.Server'])),
        ))
        db.send_create_signal('meotec', ['Site'])


    def backwards(self, orm):
        
        # Deleting model 'Manager'
        db.delete_table('meotec_manager')

        # Deleting model 'Command'
        db.delete_table('meotec_command')

        # Deleting model 'Server'
        db.delete_table('meotec_server')

        # Deleting model 'Site'
        db.delete_table('meotec_site')


    models = {
        'meotec.command': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Command'},
            'args': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meotec.manager': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Manager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'meotec.server': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Server'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'meotec.site': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repository': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meotec.Server']"})
        }
    }

    complete_apps = ['meotec']
