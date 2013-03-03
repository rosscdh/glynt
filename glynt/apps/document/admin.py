# -*- coding: UTF-8 -*-
from django.contrib import admin

from glynt.apps.document.models import DocumentTemplate, DocumentTemplateCategory, ClientCreatedDocument, DocumentHTML


class DocumentTemplateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(DocumentTemplate, DocumentTemplateAdmin)
admin.site.register([ClientCreatedDocument, DocumentHTML])