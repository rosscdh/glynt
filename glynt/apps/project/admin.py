# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from bunch import Bunch
from templated_email import send_templated_mail

from glynt.apps.project.models import Project, ProjectLawyer

import logging
logger = logging.getLogger('lawpal.project')


class ProjectLawyerInline(admin.TabularInline):
    model = ProjectLawyer
    extra = 2


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectLawyerInline]
    list_display = ('__unicode__', 'date_created', 'date_modified')
    list_filter = ['status', 'transactions']
    search_fields = ('company', 'customer', 'lawyers', 'transactions')

    def get_queryset(self, request):
        qs = Project.objects.select_related('company', 'customer', 'customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()

        my_urls = patterns(
            '',
            url(
                r'^(.+)/send_matches_email/$',
                self.admin_site.admin_view(self.send_matches_email_view),
                name='project_project_send_matches_email'
            ),
        )

        return my_urls + urls

    def send_matches_email_view(self, request, object_id, extra_context=None):
        "The 'send matches email' admin view for this model."
        model = self.model
        project = get_object_or_404(self.get_queryset(request), pk=unquote(object_id))

        client = project.customer.user
        lawyers = project.lawyers.all()

        logger.info('Sending project matches email')

        recipient = '"{name}" <{email}>'.format(name=client.get_full_name(), email=client.email)

        email = Bunch(
            template_name='project_matches',
            from_email='"LawPal ({company})" <noreply@lawpal.com>'.format(company=project.company),
            recipient_list=[recipient],
            bcc=['founders@lawpal.com'],
            context={
                'lawyers': lawyers,
                'url': reverse('dashboard:overview'),
            }
        )

        if settings.DEBUG:
            email.pop('bcc')

        send_templated_mail(**email)

        post_url = reverse('admin:project_project_changelist', current_app=self.admin_site.name)

        return HttpResponseRedirect(post_url)


class ProjectLawyerAdmin(admin.ModelAdmin):
    list_display = ('project', 'lawyer', 'display_status',)
    list_filter = ['status']
    search_fields = ('project', 'lawyer',)

    def get_queryset(self, request):
        qs = ProjectLawyer.objects.select_related('project__company', 'project__customer', 'project__customer__user').all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectLawyer, ProjectLawyerAdmin)
