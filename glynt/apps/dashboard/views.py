# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView

from bunch import Bunch

from glynt.apps.project.services.project_service import VisibleProjectsService
from glynt.apps.project.bunches import ProjectIntakeFormIsCompleteBunch
from glynt.apps.project.models import Project


class DashboardView(TemplateView):
    template_name = 'dashboard/overview.html'

    def dispatch(self, request, *args, **kwargs):
        """ if we are a lawyer, then use the lawyer overview template"""
        if 'uuid' not in kwargs:
            if request.user.profile.is_lawyer:
                self.template_name = 'dashboard/overview-lawyer.html'

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def qs_filter(self):
        project_uuid = self.request.GET.get('p', self.kwargs.get('uuid'))
        qs_filter = {}

        if project_uuid is not None:
            qs_filter = {'uuid': project_uuid}

        if self.request.user.profile.is_customer:
            qs_filter.update({
                'customer': self.request.user.customer_profile
            })

        if self.request.user.profile.is_lawyer:
            qs_filter.update({
                'lawyers': self.request.user.lawyer_profile
            })

        return qs_filter

    def get_context_data(self, **kwargs):
        qs_filter = self.qs_filter()
        project_service = VisibleProjectsService(user=self.request.user)
        current_project = project_service.project(**qs_filter)
        profile_is_complete = False

        if current_project is None:
            raise Http404('Project uuid: %s does not exist' % qs_filter.get('uuid'))
        else:
            intake_complete = ProjectIntakeFormIsCompleteBunch(project=current_project)
            profile_is_complete = intake_complete.is_valid()

        projects = Bunch({
            'project': current_project,
            'projects': project_service.get(),
            'profile_is_complete': profile_is_complete,
            'num_unread': Project.objects.new(**qs_filter).count(),
            'num_pending': Project.objects.open(**qs_filter).count(),
            'num_closed': Project.objects.closed(**qs_filter).count(),
        })
        projects.num_total = projects.num_unread + projects.num_pending + projects.num_closed

        kwargs.update(projects)
        return kwargs