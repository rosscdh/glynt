# -*- coding: utf-8 -*-
from glynt.apps.project.models import Project, ProjectLawyer
from glynt.apps.project import PROJECT_STATUS


class VisibleProjectsService(object):
    """
    Retrieve projects that are visible in the users
    Project list dropdown.
    Cater projects being from a lawyer or a customer user_class
    """
    projects = []
    project = None

    def __init__(self, *args, **kwargs):
        projects = self.projects
        project = self.project

        self.user = kwargs.get('user', None)

        if self.user is not None and self.user.is_authenticated() and not self.user.is_staff and not self.user.is_superuser:

            if self.user.profile.is_lawyer:

                projects = [join.project for join in ProjectLawyer.objects.assigned(lawyer=self.user.lawyer_profile)]
                try:
                    project = projects[0]
                except IndexError:
                    pass

            elif self.user.profile.is_customer:

                projects = Project.objects.current(customer=self.user.customer_profile)
                try:
                    project = projects[0]
                except IndexError:
                    pass

        if projects:
            self.projects = projects
        if project:
            self.project = project

        def get(self):
            return (self.projects, self.project, )