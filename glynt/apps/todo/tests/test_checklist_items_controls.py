# -*- coding: utf-8 -*-
"""
"""
from glynt.casper import BaseLawyerCustomerProjectCaseMixin, for_all_methods, glynt_mock_http_requests
from django.core.urlresolvers import reverse


@for_all_methods(glynt_mock_http_requests)
class ChecklistLawyerDetailControlsTest(BaseLawyerCustomerProjectCaseMixin):
    def test_lawyer_detail_controls_js(self):
        self.client.login(username=self.lawyer_user.username, password=self.password)

        url = reverse('todo:item', kwargs={'project_uuid': self.project.uuid, 'slug': self.todo.slug})
        self.assertTrue(self.load_casper_file(js_file='todo-item-detail-controls.js', test_label='Test the Checklist Detail.', url=url))
