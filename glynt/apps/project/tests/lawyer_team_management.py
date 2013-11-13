# -*- coding: UTF-8 -*-
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, for_all_methods, glynt_mock_http_requests
from model_mommy import mommy


@for_all_methods(glynt_mock_http_requests)
class LawyerProjectTeamManagementTest(BaseLawyerCustomerProjectCaseMixin):

    def test_lawyer_team_management_js(self):
        """
        Test the team management interface
        """
        self.client.login(username=self.lawyer_user.username, password=self.password)
        new_user = mommy.make('auth.User', username='linda-russo', first_name='Linda', last_name='Russo', email='lindajrusso@dayrep.com')

        url = reverse('dashboard:project', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='lawyer-team-management.js', test_label='Test the Lawyer can manage the project team', url=url))
