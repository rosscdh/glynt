# -*- coding: utf-8 -*-
from django.conf import settings

from notifications import notify

from glynt.apps.company.services import EnsureFounderService, EnsureCompanyService
from glynt.apps.engage.models import Engagement

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

        engagement, is_new = self.save_engagement()

        self.notify(self.engagement, is_new)

        return self.engagement

    def save_engagement(self):
        self.engagement, is_new = Engagement.objects.get_or_create(startup=self.startup, founder=self.founder, lawyer=self.lawyer)
        self.engagement.data = self.data
        self.engagement.save(update_fields=['data'])
        return self.engagement, is_new


    def notify(self, engagement, is_new):
        verb = engagement_action = 'engagement_updated'
        description = '%s Updated the Engagement Lead for %s' % (self.founder, self.lawyer,)

        if is_new:
            verb = engagement_action = 'engagement_created'
            description = '%s Created a new Lead for %s' % (self.founder, self.lawyer,)

        notify.send(self.founder.user, recipient=self.lawyer.user, verb=verb, action_object=self.engagement,
                    description=description , target=self.lawyer, engagement_action=engagement_action, engagement_pk=self.engagement.pk, lawyer_pk=self.lawyer.user.pk, founder_pk=self.founder.user.pk)