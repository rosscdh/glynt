# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DocumentTemplate.doc_category'
        db.add_column('document_documenttemplate', 'doc_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['document.DocumentTemplateCategory'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field doc_cats on 'DocumentTemplate'
        db.delete_table('document_documenttemplate_doc_cats')

        # Deleting field 'DocumentTemplateCategory.rght'
        db.delete_column('document_documenttemplatecategory', 'rght')

        # Deleting field 'DocumentTemplateCategory.parent'
        db.delete_column('document_documenttemplatecategory', 'parent_id')

        # Deleting field 'DocumentTemplateCategory.lft'
        db.delete_column('document_documenttemplatecategory', 'lft')

        # Deleting field 'DocumentTemplateCategory.active'
        db.delete_column('document_documenttemplatecategory', 'active')

        # Deleting field 'DocumentTemplateCategory.level'
        db.delete_column('document_documenttemplatecategory', 'level')

        # Deleting field 'DocumentTemplateCategory.tree_id'
        db.delete_column('document_documenttemplatecategory', 'tree_id')


        # Changing field 'DocumentTemplateCategory.slug'
        db.alter_column('document_documenttemplatecategory', 'slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=32))
        # Adding unique constraint on 'DocumentTemplateCategory', fields ['slug']
        db.create_unique('document_documenttemplatecategory', ['slug'])


        # Changing field 'DocumentTemplateCategory.name'
        db.alter_column('document_documenttemplatecategory', 'name', self.gf('django.db.models.fields.CharField')(max_length=24))

    def backwards(self, orm):
        # Removing unique constraint on 'DocumentTemplateCategory', fields ['slug']
        db.delete_unique('document_documenttemplatecategory', ['slug'])

        # Deleting field 'DocumentTemplate.doc_category'
        db.delete_column('document_documenttemplate', 'doc_category_id')

        # Adding M2M table for field doc_cats on 'DocumentTemplate'
        db.create_table('document_documenttemplate_doc_cats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documenttemplate', models.ForeignKey(orm['document.documenttemplate'], null=False)),
            ('documenttemplatecategory', models.ForeignKey(orm['document.documenttemplatecategory'], null=False))
        ))
        db.create_unique('document_documenttemplate_doc_cats', ['documenttemplate_id', 'documenttemplatecategory_id'])


        # User chose to not deal with backwards NULL issues for 'DocumentTemplateCategory.rght'
        raise RuntimeError("Cannot reverse this migration. 'DocumentTemplateCategory.rght' and its values cannot be restored.")
        # Adding field 'DocumentTemplateCategory.parent'
        db.add_column('document_documenttemplatecategory', 'parent',
                      self.gf('mptt.fields.TreeForeignKey')(related_name='children', null=True, to=orm['document.DocumentTemplateCategory'], blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'DocumentTemplateCategory.lft'
        raise RuntimeError("Cannot reverse this migration. 'DocumentTemplateCategory.lft' and its values cannot be restored.")
        # Adding field 'DocumentTemplateCategory.active'
        db.add_column('document_documenttemplatecategory', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'DocumentTemplateCategory.level'
        raise RuntimeError("Cannot reverse this migration. 'DocumentTemplateCategory.level' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'DocumentTemplateCategory.tree_id'
        raise RuntimeError("Cannot reverse this migration. 'DocumentTemplateCategory.tree_id' and its values cannot be restored.")

        # Changing field 'DocumentTemplateCategory.slug'
        db.alter_column('document_documenttemplatecategory', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'DocumentTemplateCategory.name'
        db.alter_column('document_documenttemplatecategory', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'document.clientcreateddocument': {
            'Meta': {'ordering': "['-created_at', 'name']", 'unique_together': "(('slug', 'owner'),)", 'object_name': 'ClientCreatedDocument'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'doc_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'db_column': "'data'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'meta_data': ('jsonfield.fields.JSONField', [], {'default': '{}', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True'}),
            'source_document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.DocumentTemplate']"})
        },
        'document.documenthtml': {
            'Meta': {'object_name': 'DocumentHTML'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.ClientCreatedDocument']"}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'document.documenttemplate': {
            'Meta': {'ordering': "['name']", 'object_name': 'DocumentTemplate'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'doc_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['document.DocumentTemplateCategory']", 'null': 'True', 'blank': 'True'}),
            'doc_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'document.documenttemplatecategory': {
            'Meta': {'object_name': 'DocumentTemplateCategory'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['document']