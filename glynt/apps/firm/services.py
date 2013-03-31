# -*- coding: utf-8 -*-
from models import Firm, Office

import logging
logger = logging.getLogger('lawpal.services')


class EnsureFirmService(object):
    """ Setup a Firm and at least 1 related Office """
    firm = None
    def __init__(self, firm_name, offices=[], **kwargs):
        self.firm_name = firm_name
        # ensure a list
        self.offices = [offices] if type(offices) is not list else offices

        self.data = kwargs
        self.user = self.data.pop('user', None)
        self.lawyer = self.data.pop('lawyer', None)
        # self.office_address = kwargs.pop('office_address', None)
        # self.office_phone = kwargs.pop('office_phone', None)
        # business rule
        self.create_office = self.data.get('create_office', True)
        logger.info('create_office %s'%self.create_office)

    def process(self):
        self.firm, firm_is_new = Firm.objects.get_or_create(name=self.firm_name)
        logger.info('get_or_create:firm %s is_new: %s' % (self.firm.name, firm_is_new,))

        if self.lawyer is not None:
            # removeall current associated firms, as a lawyer can have only 1 association
            self.user.firm_lawyers.remove()
            # Add user as a lawyer to this firm
            self.firm.lawyers.add(self.user)
            logger.info('Associating Lawyer %s with Firm %s'%(self.user, self.firm,))

        if self.offices is not None and self.create_office is True:
            for i,o in enumerate(self.offices):
                try:
                    office = self.firm.office_set.get(address=o)
                    office_is_new = False
                except Office.DoesNotExist,AttributeError:
                    # add office
                    office_data = {'phone': ''}
                    office, office_is_new = Office.objects.get_or_create(firm=self.firm, address=o)
                    office.data = office_data
                    office.save()

                logger.info('get_or_create:firm:office %s %s is_new: %s' % (self.firm.name, office.address, office_is_new,))
