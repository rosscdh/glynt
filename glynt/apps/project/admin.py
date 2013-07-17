# -*- coding: UTF-8 -*-
from django.contrib import admin

from glynt.apps.project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['status', 'transactions']
    list_display = ('__unicode__', 'date_created', 'date_modified')
    search_fields = ('company', 'customer', 'lawyers', 'transactions')

    def queryset (self, request):
        qs = Project.objects.select_related('company', 'customer', 'customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Project, ProjectAdmin)