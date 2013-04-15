# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import Firm, Office


class FirmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
#    list_filter = ['role']
    list_display = ('name', 'slug', 'summary')
    search_fields = ('name', 'slug', 'summary')
    order = ('name')

admin.site.register(Firm, FirmAdmin)
admin.site.register([Office])
