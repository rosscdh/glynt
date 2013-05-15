# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db.models import Count

from models import Firm, Office


class OfficeInline(admin.TabularInline):
    model = Office
    extra = 1


class FirmAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'summary', 'num_offices')
    search_fields = ('name', 'summary')
    order = ('name')
    filter_horizontal = ('lawyers', 'deals',)
    inlines = [
        OfficeInline,
    ]



admin.site.register(Firm, FirmAdmin)
admin.site.register([Office])
