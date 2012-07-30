# -*- coding: UTF-8 -*-
from django.contrib import admin
from categories.admin import CategoryBaseAdmin

from models import Document, DocumentCategory


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class DocumentCategoryAdmin(CategoryBaseAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
