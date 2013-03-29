# -*- coding: utf-8 -*-
from models import Firm, Office

import logging
logger = logging.getLogger('lawpal.services')


class EnsureFirmService(object):
    """ Setup a Firm and at least 1 related Office """
    def __init__(self, firm_name, offices, **kwargs):
        self.firm_name = firm_name
        # ensure a list
        self.offices = [offices] if type(offices) is not list else offices

        self.data = kwargs

        self.office_address = kwargs.get('office_address', None)
        self.office_phone = kwargs.get('office_phone', None)

    def process(self):
        firm, firm_is_new = Firm.objects.get_or_create(name=self.firm_name)
        logger.info('get_or_create:firm %s is_new: %s' % (firm.name, firm_is_new,))

        if self.office_address is not None:
            for i,o in enumerate(self.offices):
                try:
                    office = firm.office_set.get(address=self.office_address)
                    office_is_new = False
                except Office.DoesNotExist,AttributeError:
                    # add office
                    office_data = {'phone': office_phone}
                    office, office_is_new = Office.objects.get_or_create(firm=firm, address=self.office_address, data=office_data)

                logger.info('get_or_create:firm:office %s %s is_new: %s' % (firm.name, office.address, office_is_new,))
