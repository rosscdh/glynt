# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, for_all_methods, glynt_mock_http_requests


@for_all_methods(glynt_mock_http_requests)
class LawyerProjectDiscussionTest(BaseLawyerCustomerProjectCaseMixin):
    def test_lawyer_discussion_js(self):
        """
        Test the team management interface
        """
        self.client.login(username=self.lawyer_user.username, password=self.password)

        url = reverse('dashboard:project', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='lawyer-new-discussion.js', test_label='Test the Lawyer can discuss at the project level', url=url))
