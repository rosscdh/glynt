# -*- coding: utf-8 -*-
"""
@TODO set test descriptor
"""

import os

from django.core.urlresolvers import reverse
from model_mommy import mommy

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin


class TransactionBuilderTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_remove_founder_region_js(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('transact:builder', kwargs={ 'project_uuid': self.project.uuid, 'tx_range': 'CS', 'step': 1 })
        self.assertTrue(self.load_casper_file(js_file='founder-region.js', test_label='Test the founder region', url=url))