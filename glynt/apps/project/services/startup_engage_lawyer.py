# -*- coding: utf-8 -*-
from django.conf import settings

from notifications import notify

from glynt.apps.company.services import EnsureFounderService, EnsureCompanyService
from glynt.apps.project.models import Project

import logging
logger = logging.getLogger('lawpal.services')

site_email = settings.DEFAULT_FROM_EMAIL


class EngageLawyerAsCompanyService(object):
    """ Allow a startup to engage a Lawyer """

    def __init__(self, user, lawyer, startup_name, **kwargs):
        self.user = user
        self.lawyer = lawyer
        self.startup_name = startup_name

        self.form = kwargs.pop('form', None)

        self.data = kwargs

    def process(self):
        founder_service = EnsureFounderService(user=self.user, **self.data)
        self.founder = founder_service.process()

        startup_service = EnsureCompanyService(name=self.startup_name, founder=self.founder, **self.data)
        self.startup = startup_service.process()

        project, is_new = self.save_project()

        self.notify(self.project, is_new)

        return self.project

    def save_project(self):
        self.project, is_new = Project.objects.get_or_create(startup=self.startup, founder=self.founder, lawyer=self.lawyer)
        self.project.data = self.data
        self.project.save(update_fields=['data'])
        return self.project, is_new


    def notify(self, project, is_new):
        verb = project_action = 'project_updated'
        description = '%s Updated the Project Lead for %s' % (self.founder, self.lawyer,)

        if is_new:
            verb = project_action = 'project_created'
            description = '%s Created a new Lead for %s' % (self.founder, self.lawyer,)

        notify.send(self.founder.user, recipient=self.lawyer.user, verb=verb, action_object=self.project,
                    description=description , target=self.lawyer, project_action=project_action, project_pk=self.project.pk, lawyer_pk=self.lawyer.user.pk, founder_pk=self.founder.user.pk)