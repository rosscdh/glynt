# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from bunch import Bunch

from glynt.apps.project.models import Project
from glynt.apps.project.bunches import ProjectIntakeFormIsCompleteBunch
from glynt.apps.project import PROJECT_LAWYER_STATUS
from glynt.apps.todo.views import ToDoCountMixin


class DashboardView(ToDoCountMixin, TemplateView):
    """
    @TODO clean this mess up
    This view is used by both the customer and the lawyer (eek)
    there are some ugly rules here;
    """
    template_name = 'dashboard/overview.html'
    project_uuid = None

    def get_project_uuid(self):
        return self.kwargs.get('uuid', None)

    def dispatch(self, request, *args, **kwargs):
        """ if we are a lawyer, then use the lawyer overview template"""
        if 'uuid' in kwargs:
            self.project_uuid = self.get_project_uuid()
            self.request.session['current_project_uuid'] = self.project_uuid  # @TODO fix this codesmell encapsulate in nice method

        else:
            if request.user.profile.is_lawyer:
                self.template_name = 'dashboard/overview-lawyer.html'

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def qs_filter(self):
        qs_filter = {}

        if self.project_uuid is not None:
            qs_filter = {'uuid': self.project_uuid}

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
        return Bunch({
            'project_lawyer_joins': self.request.user.lawyer_profile.projectlawyer_set.all(),
        })

    def customer_context(self, project):
        profile_is_complete = False

        if project is not None:
            intake_complete = ProjectIntakeFormIsCompleteBunch(project=project)
            profile_is_complete = intake_complete.is_valid()

        return {
            'profile_is_complete': profile_is_complete,
        }

    def get_context_data(self, **kwargs):
        """
        is lawyer + no uuid = show lawyer project list
        is lawyer + has uuid = show project overview
        is customer + no uuid = show default project overview (customer must have at least 1 project)
        is customer + has uuid = show default project overview (customer must have at least 1 project)
        """
        qs_filter = self.qs_filter()

        if self.project_uuid is None:
            project = self.request.project
            #
            # if we are a customer and no project is present, due to an admin
            # deleting my project then rase an http.
            # not for lawyers because they need to see the projects listing when
            # they hit this view
            #
            if self.request.user.profile.is_customer and project is None:
                raise Http404
        else:
            project = get_object_or_404(Project, uuid=self.project_uuid)

        if project is not None:
            kwargs.update({
                'project': project,
            })

            # append counts
            kwargs.update(self.todo_counts(qs_objects=project.todo_set, project=project))

        if self.request.user.profile.is_customer:
            kwargs.update(
                self.customer_context(project=project)
            )

        elif self.request.user.profile.is_lawyer:
            kwargs.update(self.lawyer_context())

        kwargs.update({
            'PROJECT_LAWYER_STATUS': PROJECT_LAWYER_STATUS,
            'projects': self.request.projects,
        })

        return kwargs
