# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from glynt.apps.project.models import Project

import logging
logger = logging.getLogger('django.request')


class FounderLoginLogic(object):

    def __init__(self, user):
        self.user = user

    def redirect(self):
        try:
            founder = self.user.founder_profile
        except ObjectDoesNotExist:
            founder = None
            logger.error("founder profile not found for %s" % self.user)

        projects = Project.objects.filter(founder=founder)

        if projects:
            return redirect('dashboard:overview')
        else:
            return redirect('transact:packages')