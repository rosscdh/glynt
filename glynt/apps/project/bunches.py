# -*- coding: utf-8 -*-
from bunch import Bunch

from glynt.apps.company.forms import CompanyProfileForm

import logging
logger = logging.getLogger('lawpal.services')


class ProjectIntakeFormIsCompleteBunch(Bunch):
    errors = None
    def __init__(self, project):
        company = project.company
        return super(ProjectIntakeFormIsCompleteBunch, self).__init__(
                    founder_name = company.data.get('founders', {}).get('founder_name'),
                    founder_email = company.data.get('founders', {}).get('founder_email'),
                    incubator = company.data.get('incubator'),
                    current_status = company.data.get('current_status'),
                    profile_website = company.data.get('profile_website'),
                    description = company.data.get('description'),
                    option_plan_status = company.data.get('option_plan_status'),
                    target_states_and_countries = company.data.get('target_states_and_countries'),
                    num_officers = company.data.get('num_officers'),
                    num_employees = company.data.get('num_employees'),
                    num_consultants = company.data.get('num_consultants'),
                    ip_nolonger_affiliated = company.data.get('ip_nolonger_affiliated'),
                    ip_otherthan_founder = company.data.get('ip_otherthan_founder'),
                    ip_university_affiliation = company.data.get('ip_university_affiliation'),
                )

    def is_valid(self):
        form = CompanyProfileForm(self.__dict__)
        is_valid = form.is_valid()
        self.errors = form.errors
        return is_valid