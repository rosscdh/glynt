# -*- coding: utf-8 -*-
from models import Lawyer
from glynt.apps.firm.services import EnsureFirmService

import logging
logger = logging.getLogger('lawpal.services')


class EnsureLawyerService(object):
    """ Setup a Lawyer and his related Firm and Office """
    def __init__(self, user, firm_name, offices, **kwargs):
        self.user = user
        self.firm_name = firm_name
        self.offices = offices

        self.data = kwargs
        self.role = kwargs.get('role', Lawyer.LAWYER_ROLES.associate)

    def process(self):
        lawyer, lawyer_is_new = Lawyer.objects.get_or_create(user=self.user, role=self.role, data=self.data)
        logger.info('get_or_create:lawyer %s is_new: %s' % (lawyer.user.username, lawyer_is_new,))

        firm_service = EnsureFirmService(firm_name=self.firm_name, offices=self.offices, **self.data)
        firm_service.process()
