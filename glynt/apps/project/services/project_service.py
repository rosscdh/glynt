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
        projects, project = self.anonymous()

        self.user = kwargs.get('user', None)

        if not self.user.is_authenticated():
            self.projects, self.project = self.anonymous()

        else:
            if not self.user.is_staff and not self.user.is_superuser:

                if self.user.profile.is_customer == True:
                    self.projects, self.project = self.customer()

                elif self.user.profile.is_lawyer == True:
                    self.projects, self.project = self.lawyer()

    def anonymous(self):
        return ([], None,)

    def customer(self):
        projects = Project.objects.current(customer=self.user.customer_profile)

        try:
            project = projects[0]
        except IndexError:
            project = None

        return (projects, project,)

    def lawyer(self):
        projects = [join.project for join in ProjectLawyer.objects.assigned(lawyer=self.user.lawyer_profile)]

        try:
            project = projects[0]
        except IndexError:
            project = None

        return (projects, project,)

    def get(self):
        return (self.projects, self.project, )