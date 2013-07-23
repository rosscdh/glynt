# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView

from bunch import Bunch

from glynt.apps.project.services.project_service import VisibleProjectsService
from glynt.apps.project.models import Project


class CustomerDashboardView(TemplateView):
    template_name = 'dashboard/overview.html'

    def qs_filter(self):
        project_uuid = self.request.GET.get('p', self.kwargs.get('uuid'))
        qs_filter = {}

        if project_uuid is not None:
            qs_filter = {'uuid': project_uuid}

        qs_filter.update({
            'customer': self.request.user.customer_profile
        })
        return qs_filter

    def get_context_data(self, **kwargs):
        qs_filter = self.qs_filter()
        project_service = VisibleProjectsService(user=self.request.user)
        current_project = project_service.project(**qs_filter)

        if current_project is None:
            raise Http404('Project uuid: %s does not exist' % qs_filter.get('uuid'))

        projects = Bunch({
            'project': current_project,
            'projects': project_service.get(),
            'num_unread': Project.objects.new(**qs_filter).count(),
            'num_pending': Project.objects.open(**qs_filter).count(),
            'num_closed': Project.objects.closed(**qs_filter).count(),
        })
        projects.num_total = projects.num_unread + projects.num_pending + projects.num_closed

        kwargs.update(projects)
        return kwargs
