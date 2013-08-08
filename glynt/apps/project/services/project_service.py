# -*- coding: utf-8 -*-
from glynt.apps.project.models import Project


class VisibleProjectsService(object):
    """
    Retrieve projects that are visible in the users
    Project list dropdown
    """
    projects = None
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)

    def project(self, *args, **kwargs):
        try:
            return self.get(**kwargs).order_by('id')[0]
        except IndexError:
            return None

    def get(self, **kwargs):
        if self.user.profile.is_customer and 'customer' not in kwargs:
            kwargs.update({'customer': self.user.customer_profile})

        if self.projects is None:
            if self.user:
                self.projects = Project.objects.new(**kwargs).order_by('id') | Project.objects.open(**kwargs).order_by('id')
                self.projects = self.projects.select_related('company', 'customer__user', 'transactions')

        return self.projects
