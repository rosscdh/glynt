# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FlyForm.defaults'
        db.add_column('flyform_flyform', 'defaults',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'FlyForm.body'
        db.alter_column('flyform_flyform', 'body', self.gf('jsonfield.fields.JSONField')())

    def backwards(self, orm):
        # Deleting field 'FlyForm.defaults'
        db.delete_column('flyform_flyform', 'defaults')


        # Changing field 'FlyForm.body'
        db.alter_column('flyform_flyform', 'body', self.gf('django.db.models.fields.TextField')())

    models = {
        'flyform.flyform': {
            'Meta': {'object_name': 'FlyForm'},
            'body': ('jsonfield.fields.JSONField', [], {}),
            'defaults': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['flyform']