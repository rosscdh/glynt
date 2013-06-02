# -*- coding: utf-8 -*-
from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')


class StartupEngageLawyerBunch(Bunch):
    def __init__(self, founder):
        startup = founder.primary_startup
        return super(StartupEngageLawyerBunch, self).__init__(
                    first_name = founder.user.first_name,
                    last_name = founder.user.last_name,
                    startup_name = startup.name,
                    already_incorporated = founder.data.get('already_incorporated', False),
                    need_incorporation = founder.data.get('need_incorporation', False),
                    already_raised_capital = founder.data.get('already_raised_capital', False),
                    process_raising_capital = founder.data.get('process_raising_capital', False),
                    incubator_or_accelerator_name = founder.data.get('incubator_or_accelerator_name'),
                )
