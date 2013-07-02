# -*- coding: utf-8 -*-
from bunch import Bunch

from glynt.apps.company.forms import CompanyProfileIsCompleteValidator

import logging
logger = logging.getLogger('lawpal.services')


class CompanyEngageLawyerBunch(Bunch):
    def __init__(self, founder):
        startup = founder.primary_startup
        return super(CompanyEngageLawyerBunch, self).__init__(
                    first_name = founder.user.first_name,
                    last_name = founder.user.last_name,
                    startup_name = startup.name,
                    already_incorporated = founder.data.get('already_incorporated', False),
                    need_incorporation = founder.data.get('need_incorporation', False),
                    already_raised_capital = founder.data.get('already_raised_capital', False),
                    process_raising_capital = founder.data.get('process_raising_capital', False),
                    incubator_or_accelerator_name = founder.data.get('incubator_or_accelerator_name'),
                )

    def is_valid(self):
        form = CompanyProfileIsCompleteValidator({'first_name': self.first_name, 'last_name': self.last_name, 'startup_name': self.startup_name})
        return form.is_valid()