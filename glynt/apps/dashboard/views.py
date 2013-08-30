# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView

from bunch import Bunch

from glynt.apps.project.services.project_service import VisibleProjectsService
from glynt.apps.project.bunches import ProjectIntakeFormIsCompleteBunch
from glynt.apps.project.models import Project
from glynt.apps.project import PROJECT_LAWYER_STATUS
from glynt.apps.todo.views import ToDoCountMixin


class DashboardView(ToDoCountMixin, TemplateView):
    """
    @TODO clean this mess up
    This view is used by both the customer and the lawyer (eek)
    there are some ugly rules here;
    """
    template_name = 'dashboard/overview.html'

    def dispatch(self, request, *args, **kwargs):
        """ if we are a lawyer, then use the lawyer overview template"""
        if 'uuid' not in kwargs:
            if request.user.profile.is_lawyer:
                self.template_name = 'dashboard/overview-lawyer.html'

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def qs_filter(self):
        project_uuid = self.kwargs.get('uuid')

        qs_filter = {}

        if project_uuid is not None:
            qs_filter = {'uuid': project_uuid}

        if self.request.user.profile.is_customer:
            qs_filter.update({
                'customer': self.request.user.customer_profile
            })

        elif self.request.user.profile.is_lawyer:
            qs_filter.update({
                'lawyers': self.request.user.lawyer_profile
            })

        return qs_filter

    def lawyer_context(self):
        return Bunch({})

    def customer_context(self, project):
        intake_complete = ProjectIntakeFormIsCompleteBunch(project=self.request.project)
        profile_is_complete = intake_complete.is_valid()

        return Bunch({
                        'profile_is_complete': profile_is_complete,
                  })
        
    def get_context_data(self, **kwargs):
        profile_is_complete = False
        qs_filter = self.qs_filter()

        kwargs.update({
            'PROJECT_LAWYER_STATUS': PROJECT_LAWYER_STATUS,
            'projects': self.request.projects,
            'project': self.request.project,
        })

        if self.request.project:
            # append counts
            kwargs.update(self.todo_counts(qs_objects=self.request.project.todo_set, project=self.request.project))

        if self.request.user.profile.is_customer:

            if self.request.project is None:
                raise Http404('Project uuid: %s does not exist' % qs_filter.get('uuid'))

            kwargs.update(
                self.customer_context(project=self.request.project)
            )

        elif self.request.user.profile.is_lawyer:

            kwargs.update(self.lawyer_context())

        return kwargs