# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from glynt.apps.project.models import Project

import logging
logger = logging.getLogger('django.request')


class CustomerLoginLogic(object):

    def __init__(self, user):
        self.user = user

    def redirect(self):
        try:
            customer = self.user.customer_profile
        except ObjectDoesNotExist:
            customer = None
            logger.error("founder profile not found for %s" % self.user)

        projects = Project.objects.filter(customer=customer)

        if projects:
            return redirect('dashboard:overview')
        else:
            return redirect('project:create')