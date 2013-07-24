# -*- coding: utf-8 -*-
from bunch import Bunch

from glynt.apps.company.services import EnsureCompanyService

import json
import logging
logger = logging.getLogger('lawpal.services')


class UserIntakeCompanyBunch(Bunch):
    """
    Bunch used to process intake form company data
    """
    def __init__(self, user, **kwargs):
        self.user = user
        self.__dict__.update(kwargs)

    def as_json(self):
        return json.dumps(self.__dict__)

    def company(self):
        try:
            company = self.user.companies.all()[0]
        except IndexError:
            logger.error('Company not found for UserIntakeCompanyBunch user: "%s"' % (self.user,)) 
            company = None

        return company

    def get_data_bag(self):
        company = self.company()
        return company.data if company else {}

    def save(self, **kwargs):
        company = self.company()
        if company:
            company_service = EnsureCompanyService(name=company.name, customer=self.user.customer_profile, **kwargs)
            company_service.process()

#@TODO EVALUATE REMOVE?
class CompanyProfileBunch(Bunch):
    def __init__(self, startup):
        data = startup.data
        return super(CompanyProfileBunch, self).__init__(
                    status = data.get('status'),
                    community_profile =  False, 
                    crunchbase_url =  data.get('crunchbase_url'), 
                    video_url =  data.get('video_url'), 
                    angellist_url = data.get('angellist_url'),
                    high_concept = data.get('high_concept'),
                    locations = [i.get('display_name') for i in data.get('locations', [])],
                    markets =  [i.get('display_name') for i in data.get('markets', [])],
                    thumb_url = data.get('thumb_url'),
                    photo_url = data.get('photo_url'),
                    screenshots = [s for s in data.get('screenshots', [])],
                    already_incorporated = data.get('already_incorporated', False),
                    already_raised_capital = data.get('already_raised_capital', False),
                    process_raising_capital = data.get('process_raising_capital', False),
                    incubator_or_accelerator_name = data.get('incubator_or_accelerator_name'),
                )