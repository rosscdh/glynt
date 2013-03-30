# -*- coding: utf-8 -*-
from models import Lawyer
from glynt.apps.firm.services import EnsureFirmService

import logging
logger = logging.getLogger('lawpal.services')


class EnsureLawyerService(object):
    """ Setup a Lawyer and his related Firm and Office """
    lawyer = None
    firm = None
    def __init__(self, user, firm_name, offices, **kwargs):
        self.user = user
        self.firm_name = firm_name
        self.offices = offices

        self.role = kwargs.pop('role', Lawyer.LAWYER_ROLES.associate)
        self.data = kwargs
        logger.debug(self.data)

    def process(self):
        self.lawyer, lawyer_is_new = Lawyer.objects.get_or_create(user=self.user)
        if self.role:
            self.lawyer.role = self.role
        if self.data:
            self.lawyer.data = self.data

        self.lawyer.save()

        logger.info('get_or_create:lawyer %s is_new: %s' % (self.lawyer.user.username, lawyer_is_new,))

        self.data.update({'user': self.user,'lawyer': self.lawyer})

        if self.firm_name is not None:
            firm_service = EnsureFirmService(firm_name=self.firm_name, offices=self.offices, **self.data)
            firm_service.process()
            self.firm = firm_service.firm
        else:
            logger.info('Firm name not provided for lawyer %s ' % (self.lawyer.user.username,))
            # usermay already be associated with a firm
            firms = self.user.firm_lawyers.all()
            if firms:
                self.firm = firms[0]
                logger.info('Firm %s is assocaited with lawyer %s ' % (self.lawyer.user.username, self.firm.name))
            
