# -*- coding: UTF-8 -*-
from django.contrib import admin

from glynt.apps.engage.models import Engagement


class EngagementAdmin(admin.ModelAdmin):
    list_filter = ['engagement_status']
    list_display = ('__unicode__', 'date_created')
    search_fields = ('startup', 'founder', 'lawyer')

admin.site.register(Engagement, EngagementAdmin)