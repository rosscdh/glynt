# -*- coding: utf-8 -*-
from models import Firm

import logging
logger = logging.getLogger('lawpal.services')


class EnsureFirmService(object):
    """ Setup a Firm """
    firm = None
    def __init__(self, firm_name, offices=[], **kwargs):
        self.firm_name = firm_name
        # ensure a list
        self.offices = [offices] if type(offices) is not list else offices

        self.data = kwargs
        self.user = self.data.pop('user', None)
        self.lawyer = self.data.pop('lawyer', None)

    def process(self):
        self.firm, firm_is_new = Firm.objects.get_or_create(name=self.firm_name)
        logger.info('get_or_create:firm %s is_new: %s' % (self.firm.name, firm_is_new,))

        if self.lawyer is not None:
            # removeall current associated firms, as a lawyer can have only 1 association
            self.lawyer.firm_lawyers.clear()

            # Add user as a lawyer to this firm
            self.firm.lawyers.add(self.lawyer)
            logger.info('Associating Lawyer %s with Firm %s'%(self.user, self.firm,))
            self.firm.data['offices'] = self.offices
            self.firm.save(update_fields=['data'])