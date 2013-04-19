# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Firm'
        db.create_table(u'firm_firm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'firm', ['Firm'])

        # Adding M2M table for field lawyers on 'Firm'
        db.create_table(u'firm_firm_lawyers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('firm', models.ForeignKey(orm[u'firm.firm'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'firm_firm_lawyers', ['firm_id', 'user_id'])

        # Adding M2M table for field deals on 'Firm'
        db.create_table(u'firm_firm_deals', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('firm', models.ForeignKey(orm[u'firm.firm'], null=False)),
            ('deal', models.ForeignKey(orm[u'deal.deal'], null=False))
        ))
        db.create_unique(u'firm_firm_deals', ['firm_id', 'deal_id'])

        # Adding model 'Office'
        db.create_table(u'firm_office', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['firm.Firm'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('country', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'firm', ['Office'])

        # Adding model 'tmpLawyerFirm'
        db.create_table(u'firm_tmplawyerfirm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'firm', ['tmpLawyerFirm'])


    def backwards(self, orm):
        # Deleting model 'Firm'
        db.delete_table(u'firm_firm')

        # Removing M2M table for field lawyers on 'Firm'
        db.delete_table('firm_firm_lawyers')

        # Removing M2M table for field deals on 'Firm'
        db.delete_table('firm_firm_deals')

        # Deleting model 'Office'
        db.delete_table(u'firm_office')

        # Deleting model 'tmpLawyerFirm'
        db.delete_table(u'firm_tmplawyerfirm')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'deal.deal': {
            'Meta': {'object_name': 'Deal'},
            'date_finalized': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'deal_type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lawyer': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'deal_lawyer'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'provider': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'deal_provider'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'recipient': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'deal_recipient'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        u'firm.firm': {
            'Meta': {'object_name': 'Firm'},
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'deals': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'firm_deals'", 'blank': 'True', 'to': u"orm['deal.Deal']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lawyers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'firm_lawyers'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'firm.office': {
            'Meta': {'object_name': 'Office'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'firm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['firm.Firm']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'firm.tmplawyerfirm': {
            'Meta': {'object_name': 'tmpLawyerFirm'},
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['firm']