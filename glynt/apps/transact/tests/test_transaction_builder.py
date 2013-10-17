# -*- coding: utf-8 -*-
"""
@TODO set test descriptor
"""
from django.core.urlresolvers import reverse

import os

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin


class TransactionBuilderTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_form_builder(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })

        resp = self.client.get(url)
        css = self.pq(resp.content)
        form_object = css('form#builder-form')
        csrfmiddlewaretoken = css.find('input[type="hidden"][name="csrfmiddlewaretoken"]')[0].value

        form_values = {
            "builder_wizard_view-current_step": "1",
            "csrfmiddlewaretoken": "WGWuAzotnfzpZbilR5skCokwIOc23dGj",
            "1-form_json_data": '{"ip_otherthan_founder":true,"description":"","option_plan_status":"2","num_employees":"2","founder_name":"Ross Crawford","num_consultants":"1","target_states_and_countries":"California","incubator":"FoundersDen","num_option_holders":"0","ip_university_affiliation":false,"company_name":"LawPal.com","founder_email":"ross@lawpal.com","founders":{"founder_name":{"id":"founder_name","val":"Ross Crawford","name":"founder_name"},"founder_email":{"id":"founder_email","val":"ross@lawpal.com","name":"founder_email"}},"ip_nolonger_affiliated":false,"profile_website":"http://angel.com/lawpal","current_status":"1","num_officers":"22","profile_is_complete":true}',
            "1-founder_name": "Ross Crawford",
            "1-founder_email": "ross@lawpal.com",
            "1-incubator": "FoundersDen",
            "1-current_status": "1",
            "1-current_status": "2",
            "1-current_status": "3",
            "1-current_status": "4",
            "1-profile_website": "http://angel.com/lawpal",
            "1-description": "",
            "1-target_states_and_countries": "California",
            "1-num_officers": "22",
            "1-num_employees": "2",
            "1-num_consultants": "1",
            "1-option_plan_status": "1",
            "1-option_plan_status": "2",
            "1-option_plan_status": "3",
            "1-num_option_holders": "0",
            "1-ip_nolonger_affiliated": "on",
            "1-ip_otherthan_founder": "on",
            "1-ip_university_affiliation": "on",
        }

        # post and return the response for evaluation
        resp = self.client.post(url, form_values, follow=True)
        self.assertEqual(200, resp.status_code)

        css = self.pq(resp.content)
        form_object = css('form#builder-form')

        for field in form_object.find('input'):
            if field.name in form_values:
                self.assertEqual(field.value, form_values[field.name])

    def test_form_builder_js(self):
        self.client.login(username=self.customer_user.username, password=self.password)
        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })
        self.assertTrue(self.load_casper_file(js_file='transact-builder-form.js', test_label='Test the form completes successfully', url=url))

    def test_remove_founder_region_js(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })
        self.assertTrue(self.load_casper_file(js_file='founder-region.js', test_label='Test the founder region', url=url))