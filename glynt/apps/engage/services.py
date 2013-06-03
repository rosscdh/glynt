# -*- coding: utf-8 -*-
import os

try:
    from notification import models as notification
except:
    notification = None
from glynt.apps.startup.services import EnsureFounderService, EnsureStartupService
from models import Engagement


import logging
logger = logging.getLogger('lawpal.services')


class EngageLawyerAsStartupService(object):
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

        startup_service = EnsureStartupService(name=self.startup_name, founder=self.founder, **self.data)
        startup = startup_service.process()

        engagement, is_new = Engagement.objects.get_or_create(startup=startup, founder=self.founder, lawyer=self.lawyer)
        engagement.data = self.data
        engagement.save(update_fields=['data'])

        self.notify(engagement, is_new)

        return engagement

    def notify(self, engagement, is_new):
        action = 'engagement_request_update'
        if is_new:
            action = 'engagement_request_new'

        notification.send([self.lawyer.user], action, {"from_user": self.user})