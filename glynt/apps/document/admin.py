# -*- coding: UTF-8 -*-
from django.contrib import admin

from categories.admin import CategoryBaseAdmin

from glynt.apps.document.models import DocumentTemplate, DocumentTemplateCategory, ClientCreatedDocument


class DocumentTemplateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ('Template Properties', { 'fields': ('name', 'slug', 'owner', 'acronym', 'summary', 'description', 'doc_status', 'is_public', 'doc_cats') }),
        ('Template Authoring', {'fields': ('body',), 'description': 'Author your document using the text input below. You should see a preview of the document.' }),
    )

class DocumentTemplateCategoryAdmin(CategoryBaseAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(DocumentTemplate, DocumentTemplateAdmin)
admin.site.register(DocumentTemplateCategory, DocumentTemplateCategoryAdmin)
admin.site.register([ClientCreatedDocument])