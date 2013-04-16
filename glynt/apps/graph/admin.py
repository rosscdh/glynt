# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import GraphConnection

class GraphConnectionAdmin(admin.ModelAdmin):
    list_filter = ['provider']
    list_display = ('full_name', 'provider')
    search_fields = ('full_name', 'provider')


admin.site.register(GraphConnection, GraphConnectionAdmin)

