# -*- coding: UTF-8 -*-
from django.contrib import admin

from glynt.apps.project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['project_status']
    list_display = ('__unicode__', 'date_created' ,'slug')
    search_fields = ('startup', 'customer', 'lawyer')

    def queryset (self, request):
        qs = Project.objects.select_related('startup', 'customer', 'founder__user', 'lawyer', 'lawyer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Project, ProjectAdmin)