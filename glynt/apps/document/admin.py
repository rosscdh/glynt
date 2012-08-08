# -*- coding: UTF-8 -*-
from django.contrib import admin
from categories.admin import CategoryBaseAdmin

from models import Document, DocumentCategory
from glynt.apps.flyform.models import FlyForm


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class DocumentCategoryAdmin(CategoryBaseAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register([FlyForm])