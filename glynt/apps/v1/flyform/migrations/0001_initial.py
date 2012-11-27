# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FlyForm'
        db.create_table('flyform_flyform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('flyform', ['FlyForm'])


    def backwards(self, orm):
        # Deleting model 'FlyForm'
        db.delete_table('flyform_flyform')


    models = {
        'flyform.flyform': {
            'Meta': {'object_name': 'FlyForm'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['flyform']