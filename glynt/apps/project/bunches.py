# -*- coding: utf-8 -*-
from bunch import Bunch

from glynt.apps.company.forms import CompanyProfileForm

import logging
logger = logging.getLogger('lawpal.services')


class ProjectIntakeFormIsCompleteBunch(Bunch):
    errors = None
    project = None
    company = None

    def __init__(self, project):
        self.project = project
        self.company = self.project.company
        return super(ProjectIntakeFormIsCompleteBunch, self).__init__(
                        founder_name = self.company.data.get('founders', {}).get('founder_name').get('val'),
                        founder_email = self.company.data.get('founders', {}).get('founder_email').get('val'),
                        incubator = self.company.data.get('incubator'),
                        current_status = self.company.data.get('current_status'),
                        profile_website = self.company.data.get('profile_website'),
                        description = self.company.data.get('description'),
                        option_plan_status = self.company.data.get('option_plan_status'),
                        target_states_and_countries = self.company.data.get('target_states_and_countries'),
                        num_officers = self.company.data.get('num_officers'),
                        num_employees = self.company.data.get('num_employees'),
                        num_consultants = self.company.data.get('num_consultants'),
                        num_option_holders = self.company.data.get('num_option_holders'),
                        ip_nolonger_affiliated = self.company.data.get('ip_nolonger_affiliated'),
                        ip_otherthan_founder = self.company.data.get('ip_otherthan_founder'),
                        ip_university_affiliation = self.company.data.get('ip_university_affiliation'),
                    )

    @property
    def founders(self):
        """ nasty way to coerce cloned_data into somethign useful"""
        # founders = []
        # founders_dic = self.company.data.get('founders', {})
        # for i in founders_dic.keys():
        #     pass
        return []

    def is_valid(self):
        form = CompanyProfileForm(self)
        is_valid = form.is_valid()

        if not is_valid:
            self.errors = form.errors

        return is_valid