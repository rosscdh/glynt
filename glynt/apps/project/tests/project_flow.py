# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin
from glynt.apps.transact.models import Transaction

import os


class CustomerSelectTransactionTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.dirname(__file__)

    def test_customer_transact_select_js(self):
        """
        Test that the Customer has a list of transaction types to select from
        """
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('project:create')
        self.assertTrue(self.load_casper_file(js_file='customer-transact-select.js', test_label='Test a Customer can select transactions', url=url))


class CustomerCreateProjectTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.dirname(__file__)

    def setUp(self):
        super(CustomerCreateProjectTest, self).setUp()
        # Remove the base
        self.project.transactions.clear()
        self.project.transactions.add(Transaction.objects.get(slug='CS'))
        self.project.attachments.all().delete()
        self.project.todo_set.all().delete()
        self.project_lawyer_join.delete()

    def test_customer_incorporation_form_js(self):
        """
        Test that the Customer has a list of transaction types to select from
        """
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={'project_uuid': self.project.uuid, 'tx_range': self.project.tx_range, 'step': 1})
        url_checklist = reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='customer-incorporation-form.js', test_label='Test a Customer can complete the Incorporation form', url=url, url_checklist=url_checklist))
