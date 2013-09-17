# -*- coding: utf-8 -*-
from glynt.apps.project.models import Project, ProjectLawyer
from glynt.apps.project import PROJECT_STATUS

import itertools


class VisibleProjectsService(object):
    """
    Retrieve projects that are visible in the users
    Project list dropdown.
    Cater projects being from a lawyer or a customer user_class
    """
    current_key = None
    request = None
    user = None

    projects = []
    project = None

    def __init__(self, request, *args, **kwargs):
        projects, project = self.anonymous()

        self.user = kwargs.get('user', request.user)

        self.request = request

        puid = self.request.GET.get('puid', None)
        if puid is not None:
            self.request.session['current_project_uuid'] = puid

        self.current_key = self.request.session.get('current_project_uuid')

        # not logged in
        if not self.user.is_authenticated():
            self.projects, self.project = self.anonymous()

        else:
            # they are not staff and not an admin
            if not self.user.is_staff and not self.user.is_superuser:
                # are a customer
                if self.user.profile.is_customer == True:
                    self.projects, self.project = self.customer()
                # are a lawyer
                elif self.user.profile.is_lawyer == True:
                    self.projects, self.project = self.lawyer()

    def current_project(self, projects):
        project = None

        # if we have a current key use that
        if self.current_key:
            try:
                # if its a queryset it should have get, but lists have no get
                if hasattr(projects, 'get'):
                    project = projects.get(uuid=self.current_key)

                else:
                    #  must be a lawyer at this point as we return a list and not a queryset
                    #  thus calling .get on the list will fail
                    project = [p for p in projects if p.uuid == self.current_key][0]

            except IndexError, Project.DoesNotExist:
                pass

        # we still have no project set
        if project is None:
            try:
                project = projects[0]
            except IndexError:
                project = None

        return project

    def anonymous(self):
        return ([], None,)

    def customer(self):
        projects = Project.objects.current(customer=self.user.customer_profile)
        project = self.current_project(projects)

        return (projects, project,)

    def lawyer(self):
        # project_lawyers = itertools.chain(ProjectLawyer.objects.potential(lawyer=self.user.lawyer_profile), \
        #                                   ProjectLawyer.objects.assigned(lawyer=self.user.lawyer_profile))
        project_lawyers = ProjectLawyer.objects.assigned(lawyer=self.user.lawyer_profile)
        projects = [join.project for join in project_lawyers]

        project = self.current_project(projects)

        return (projects, project,)

    def get(self):
        return (self.projects, self.project, )