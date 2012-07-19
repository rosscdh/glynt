# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import Document

class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Document, DocumentAdmin)

