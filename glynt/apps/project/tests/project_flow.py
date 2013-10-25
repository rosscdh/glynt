# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, glynt_mock_http_requests
from glynt.apps.transact.models import Transaction

import os
from model_mommy import mommy


class CustomerSelectTransactionTest(BaseLawyerCustomerProjectCaseMixin):
    test_path = os.path.dirname(__file__)

    def test_customer_transact_select_js(self):
        """
        Test that the Customer has a list of transaction types to select from
        """
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('project:create')
        self.assertTrue(self.load_casper_file(js_file='customer-transact-select.js', test_label='Test a Customer can select transactions', url=url))


class CustomerCreateProjectTest(BaseLawyerCustomerProjectCaseMixin):
    test_path = os.path.dirname(__file__)

    @glynt_mock_http_requests
    def setUp(self):
        super(CustomerCreateProjectTest, self).setUp()
        # re-create the project but without the associated todos and attachments
        # causes issues with httprettynot mocking out the crocdoc delete calls
        self.project = mommy.make('project.project', customer=self.customer, company=self.company, lawyers=(self.lawyer,), transactions=(Transaction.objects.get(slug='CS'),))

    def test_customer_incorporation_form_js(self):
        """
        Test that the Customer has a list of transaction types to select from
        """
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={'project_uuid': self.project.uuid, 'tx_range': self.project.tx_range, 'step': 1})
        url_checklist = reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='customer-incorporation-form.js', test_label='Test a Customer can complete the Incorporation form', url=url, url_checklist=url_checklist))
