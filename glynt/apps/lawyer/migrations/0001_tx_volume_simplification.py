# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

def ensure_int(input):
    if type(input) is list:
        for i,sub in enumerate(input):
            if type(sub) is dict:
                for key in sub:
                    sub[key] = int(sub[key])
                input[i] = sub
    return input

def avg_by_year(input):
    l = []
    if type(input) is dict:
        for key,value in input.items():
            l.append(value)
    if len(l) == 0:
        return 0
    else:
        return round(reduce(lambda x, y: x + y, l) / float(len(l)), 2)

def total(input):
    r = None
    if type(input) is list:
        r = sum((Counter(dict(x)) for x in input if type(x) is dict), Counter())
    if r is not None:
        return dict(r)
    else:
        return r


class Migration(DataMigration):

    def forwards(self, orm):
        "Convert the old complex volume structures to the new simpler"
        for l in orm['lawyer.Lawyer'].objects.all():

            volume_incorp_setup = l.data.get('volume_incorp_setup',{})

            volume_seed_financing = l.data.get('volume_seed_financing',{})
            #print volume_incorp_setup
            volume_series_a = l.data.get('volume_series_a',{})
            #print volume_incorp_setup
            volume_ip = l.data.get('volume_ip',{})
            #print volume_incorp_setup
            volume_other = l.data.get('volume_other',{})
            #print volume_other
            input = ensure_int([volume_incorp_setup, volume_seed_financing, volume_series_a, volume_ip, volume_other])
            #print input
            #print volume_incorp_setup
            #print t
            l.data['volume_incorp_setup'] = avg_by_year(volume_incorp_setup)
            l.data['volume_seed_financing'] = avg_by_year(volume_seed_financing)
            l.data['volume_series_a'] = avg_by_year(volume_series_a)
            l.data['volume_ip'] = avg_by_year(volume_ip)
            l.data['volume_other'] = avg_by_year(volume_other)
            l.save(update_fields=['data'])

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
        u'lawyer.lawyer': {
            'Meta': {'object_name': 'Lawyer'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'role': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'lawyer_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['lawyer']
    symmetrical = True
