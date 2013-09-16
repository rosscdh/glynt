# -*- coding: UTF-8 -*-
from django.contrib import admin

from glynt.apps.project.models import Project, ProjectLawyer


class ProjectLawyerInline(admin.TabularInline):
    model = ProjectLawyer
    extra = 2


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectLawyerInline]
    list_display = ('__unicode__', 'date_created', 'date_modified')
    list_filter = ['status', 'transactions']
    search_fields = ('company', 'customer', 'lawyers', 'transactions')

    def queryset(self, request):
        qs = Project.objects.select_related('company', 'customer', 'customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class ProjectLawyerAdmin(admin.ModelAdmin):
    list_display = ('project', 'lawyer', 'display_status',)
    list_filter = ['status']
    search_fields = ('project', 'lawyer',)

    def queryset(self, request):
        qs = ProjectLawyer.objects.select_related('project__company', 'project__customer', 'project__customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectLawyer, ProjectLawyerAdmin)
