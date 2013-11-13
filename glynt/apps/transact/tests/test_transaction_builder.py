# -*- coding: utf-8 -*-
"""
@TODO set test descriptor
"""
import os
import json

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin, for_all_methods, glynt_mock_http_requests

from glynt.apps.company.forms import (CompanyProfileForm,
                                      CompanyAndFinancingProfileForm,
                                      CompanyProfileAndIntakeForm,
                                      CompanyFinancingProfileAndIntakeForm,
                                      FinancingProfileForm,
                                      FinancingProfileAndIntakeForm,
                                      IntakeForm,
                                     )


@for_all_methods(glynt_mock_http_requests)
class TransactionBuilderTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def setUp(self):
        super(TransactionBuilderTest, self).setUp()

        self.factory = RequestFactory()

    def test_form_builder(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })

        resp = self.client.get(url)
        css = self.pq(resp.content)
        form_object = css('form#builder-form')
        csrfmiddlewaretoken = css.find('input[type="hidden"][name="csrfmiddlewaretoken"]')[0].value

        form_values = {
            "builder_wizard_view-current_step": "1",
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "1-form_json_data": '{"ip_otherthan_founder":true,"description":"","option_plan_status":"2","num_employees":"2","founder_name":"Ross Crawford","num_consultants":"1","target_states_and_countries":"California","incubator":"FoundersDen","num_option_holders":"0","ip_university_affiliation":false,"company_name":"Test Company","founder_email":"ross@lawpal.com","founders":{"founder_name":{"id":"founder_name","val":"Ross Crawford","name":"founder_name"},"founder_email":{"id":"founder_email","val":"ross@lawpal.com","name":"founder_email"}},"ip_nolonger_affiliated":false,"profile_website":"http://angel.com/lawpal","current_status":"1","num_officers":"22","profile_is_complete":true}',
            "1-founder_name": "Ross Crawford",
            "1-founder_email": "ross@lawpal.com",
            "1-incubator": "FoundersDen",
            "1-current_status": "1",
            "1-profile_website": "http://angel.com/lawpal",
            "1-description": "My Description",
            "1-target_states_and_countries": "California",
            "1-num_officers": "22",
            "1-num_employees": "2",
            "1-num_consultants": "1",
            "1-option_plan_status": "1",
            "1-num_option_holders": "0",
            "1-ip_nolonger_affiliated": "on",
            "1-ip_otherthan_founder": "on",
            "1-ip_university_affiliation": "on",
        }

        # post and return the response for evaluation
        resp = self.client.post(url, form_values, follow=True)
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(url)

        css = self.pq(resp.content)
        form_object = css('form#builder-form')

        expected_form_json_data = json.loads('{"ip_otherthan_founder": true, "num_officers": "22", "description": "My Description", "option_plan_status": "1", "num_employees": "2", "founder_email": "ross@lawpal.com", "num_consultants": "1", "target_states_and_countries": "California", "incubator": "FoundersDen", "num_option_holders": "0", "ip_university_affiliation": true, "company_name": "Test Company", "founder_name": "Ross Crawford", "founders": {"founder_name": {"id": "founder_name", "val": "Ross Crawford", "name": "founder_name"}, "founder_email": {"id": "founder_email", "val": "ross@lawpal.com", "name": "founder_email"}}, "ip_nolonger_affiliated": true, "current_status": "1", "profile_website": "http://angel.com/lawpal", "profile_is_complete": true}')
        have_checked = []

        # loop over inputs
        for field in form_object.find('input'):
            if field.name not in ['csrfmiddlewaretoken']:  # skip middleware token as it will change
                # handle radio items with have_checked
                if field.name not in have_checked and field.name in form_values:
                    # make nicer way of handeling value comparison
                    field_value = field.value
                    expected_value = form_values[field.name]

                    # handle the json field (cant cmpare strings as the order is different) must be dict
                    if field.name == '1-form_json_data':
                        field_value = json.loads(field.value)
                        expected_value = expected_form_json_data

                    self.assertEqual(field_value, expected_value)
                    # add to checked (radio items)
                    have_checked.append(field.name)

    """
    Incorporation form
    """
    def test_form_builder_incorporation(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'INC', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = CompanyProfileForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    """
    Incorporation and Financing form
    """
    def test_form_builder_incorporation_and_financing(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'INC,FIN', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = CompanyAndFinancingProfileForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    """
    Incorporation, Financing and Intake form
    """
    def test_form_builder_incorporation_financing_and_intake(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'INC,FIN,NDA', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = CompanyFinancingProfileAndIntakeForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    """
    Incorporation and Intake form
    """
    def test_form_builder_incorporation_and_intake(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'INC,NDA', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = CompanyProfileAndIntakeForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    """
    Financing form
    """
    def test_form_builder_financing(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'FIN', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = FinancingProfileForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    """
    Financing and Intake form
    """
    def test_form_builder_financing_and_intake(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'FIN,NDA', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = FinancingProfileAndIntakeForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    """
    Intake form
    """
    def test_form_builder_intake(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'NDA', 'step': 1 })

        request = self.factory.get(url)
        request.project = self.project

        form = IntakeForm(request=request)

        response = self.client.get(url)
        self.assertEqual(response.context['form'].fields.keys(), form.fields.keys());

    def test_form_builder_js(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })
        self.assertTrue(self.load_casper_file(js_file='transact-builder-form.js', test_label='Test the form completes successfully', url=url))

    def test_remove_founder_region_js(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })
        self.assertTrue(self.load_casper_file(js_file='founder-region.js', test_label='Test the founder region', url=url))