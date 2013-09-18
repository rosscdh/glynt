# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse
from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin

import os


class CustomerCreateProjectTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.dirname(__file__)

    def test_customer_transact_select_js(self):
        """
        Test that the Customer has a list of transaction types to select from
        """
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('project:create')
        self.assertTrue(self.load_casper_file(js_file='customer-transact-select.js', test_label='Test a Customer can select transactions', url=url))
