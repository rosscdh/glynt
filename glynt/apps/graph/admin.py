# -*- coding: UTF-8 -*-
from django.contrib import admin

from models import GraphConnection, FullContactData


class GraphConnectionAdmin(admin.ModelAdmin):
    list_filter = ['provider']
    list_display = ('full_name', 'provider')
    search_fields = ('full_name', 'provider')


class FullContactDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'social_profile_names', 'profile_pic',)


admin.site.register(GraphConnection, GraphConnectionAdmin)
admin.site.register(FullContactData, FullContactDataAdmin)
