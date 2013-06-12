# -*- coding: UTF-8 -*-
from django.contrib import admin

from glynt.apps.engage.models import Engagement


class EngagementAdmin(admin.ModelAdmin):
    list_filter = ['engagement_status']
    list_display = ('__unicode__', 'date_created' ,'slug')
    search_fields = ('startup', 'founder', 'lawyer')

    def queryset (self, request):
        qs = Engagement.objects.select_related('startup', 'founder', 'founder__user', 'lawyer', 'lawyer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Engagement, EngagementAdmin)