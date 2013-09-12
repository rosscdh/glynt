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


        if not self.user.is_authenticated():
            self.projects, self.project = self.anonymous()

        else:
            if not self.user.is_staff and not self.user.is_superuser:

                if self.user.profile.is_customer == True:
                    self.projects, self.project = self.customer()

                elif self.user.profile.is_lawyer == True:
                    self.projects, self.project = self.lawyer()

    def current_project(self, projects):
        project = None

        # if we have a current key use that
        if self.current_key:
            try:
                project = projects.get(uuid=self.current_key)
            except Project.DoesNotExist:
                pass

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
        project_lawyers = itertools.chain(ProjectLawyer.objects.potential(lawyer=self.user.lawyer_profile), \
                                          ProjectLawyer.objects.assigned(lawyer=self.user.lawyer_profile))
        projects = [join.project for join in project_lawyers]

        project = self.current_project(projects)

        return (projects, project,)

    def get(self):
        return (self.projects, self.project, )