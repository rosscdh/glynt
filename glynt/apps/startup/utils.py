from django.shortcuts import redirect

from glynt.apps.engage.models import Engagement

import logging
logger = logging.getLogger('django.request')


class FounderLoginLogic(object):

    def __init__(self, user):
        self.user = user

    def redirect(self):
        try:
            founder = self.user.founder_profile
        except DoesNotExist:
            founder = None
            logger.error("founder profile not found for %s" % self.user)

        engagements = Engagement.objects.filter(founder=founder)

        if engagements:
            return redirect('dashboard:overview')
        else:
            return redirect('transact:packages')