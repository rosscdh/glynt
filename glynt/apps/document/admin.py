# -*- coding: UTF-8 -*-
from django.contrib import admin

from categories.admin import CategoryBaseAdmin

from glynt.apps.document.models import Document, DocumentCategory, ClientCreatedDocument


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ('Document Properties', { 'fields': ('name', 'slug', 'owner', 'summary', 'doc_status', 'is_public', 'doc_cats', 'tags',) }),
        ('Document Authoring', {'fields': ('body',), 'description': 'Author your document using the text input below. You should see a preview of the document.' }),
    )

class DocumentCategoryAdmin(CategoryBaseAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register([ClientCreatedDocument])