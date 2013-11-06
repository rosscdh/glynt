# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin
from glynt.apps.transact.models import Transaction
from model_mommy import mommy

import os


class LawyerProjectDiscussionTest(BaseLawyerCustomerProjectCaseMixin):
    test_path = os.path.dirname(__file__)

    def test_lawyer_discussion_js(self):
        """
        Test the team management interface
        """
        self.client.login(username=self.lawyer_user.username, password=self.password)

        url = reverse('dashboard:project', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='lawyer-new-discussion.js', test_label='Test the Lawyer can discuss at the project level', url=url))
