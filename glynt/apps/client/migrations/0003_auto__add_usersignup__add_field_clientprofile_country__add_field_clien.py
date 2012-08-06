# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserSignup'
        db.create_table('client_usersignup', (
            ('userenasignup_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userena.UserenaSignup'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('client', ['UserSignup'])

        # Adding field 'ClientProfile.country'
        db.add_column('client_clientprofile', 'country',
                      self.gf('django_countries.fields.CountryField')(default='US', max_length=2, null=True),
                      keep_default=False)

        # Adding field 'ClientProfile.state'
        db.add_column('client_clientprofile', 'state',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True),
                      keep_default=False)


        # Changing field 'ClientProfile.profile_data'
        db.alter_column('client_clientprofile', 'profile_data', self.gf('jsonfield.fields.JSONField')(null=True))

    def backwards(self, orm):
        # Deleting model 'UserSignup'
        db.delete_table('client_usersignup')

        # Deleting field 'ClientProfile.country'
        db.delete_column('client_clientprofile', 'country')

        # Deleting field 'ClientProfile.state'
        db.delete_column('client_clientprofile', 'state')


        # Changing field 'ClientProfile.profile_data'
        db.alter_column('client_clientprofile', 'profile_data', self.gf('jsonfield.fields.JSONField')(default=''))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'client.clientprofile': {
            'Meta': {'object_name': 'ClientProfile'},
            'country': ('django_countries.fields.CountryField', [], {'default': "'US'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'profile_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'my_profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'client.usersignup': {
            'Meta': {'object_name': 'UserSignup', '_ormbases': ['userena.UserenaSignup']},
            'userenasignup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userena.UserenaSignup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'userena.userenasignup': {
            'Meta': {'object_name': 'UserenaSignup'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'activation_notification_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_confirmation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'email_confirmation_key_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_unconfirmed': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_active': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'userena_signup'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['client']