# -*- coding: utf-8 -*-
from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')


class TransactionBunch(Bunch):
    def __init__(self, transaction):
        startup = founder.primary_startup
        return super(TransactionBunch, self).__init__(
                    transa = founder.data.get('incubator_or_accelerator_name'),
                )

    def is_valid(self):
        form = StartupProfileIsCompleteValidator({'first_name': self.first_name, 'last_name': self.last_name, 'startup_name': self.startup_name})
        return form.is_valid()