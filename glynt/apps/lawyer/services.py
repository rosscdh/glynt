# -*- coding: utf-8 -*-
from models import Lawyer
from glynt.apps.firm.services import EnsureFirmService

import logging
logger = logging.getLogger('lawpal.services')


class EnsureLawyerService(object):
    """ Setup a Lawyer and his related Firm and Office """
    lawyer = None
    firm = None
    def __init__(self, user, firm_name=None, offices=[], **kwargs):
        self.user = user
        self.firm_name = firm_name
        self.offices = offices

        self.role = kwargs.pop('role', Lawyer.LAWYER_ROLES.associate)

        self.data = kwargs

    def process(self):
        self.lawyer, lawyer_is_new = Lawyer.objects.get_or_create(user=self.user)

        if self.role:
            self.lawyer.role = self.role

        if self.data:
            self.lawyer.data = self.data

        if self.data.get('summary', None) is not None:
            self.lawyer.summary = self.data.get('summary')

        if self.data.get('bio', None) is not None:
            self.lawyer.bio = self.data.get('bio')

        self.lawyer.save()

        logger.info('get_or_create:lawyer %s is_new: %s' % (self.lawyer.user.username, lawyer_is_new,))

        if self.firm_name is not None:

            self.data.update({
                'create_office': False, # May not create office, as the csv for Lawyers does not contain the right info.. use import_firms
                'user': self.user,
                'lawyer': self.lawyer
            })

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
            
