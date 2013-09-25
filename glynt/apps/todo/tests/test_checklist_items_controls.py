# -*- coding: utf-8 -*-
"""
"""
from glynt.casper import BaseLawyerCustomerProjectCaseMixin
from glynt.apps.todo.models import FeedbackRequest
from glynt.apps.todo import TODO_STATUS, FEEDBACK_STATUS
from model_mommy import mommy

import os
import httpretty

class ChecklistLawyerDetailControlsTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):

   def test_lawyer_detail_controls_js(self):
           self.client.login(username=self.lawyer_user.username, password=self.password)

           url = reverse('todo:item', kwargs={'uuid': self.project.uuid, 'slug':self.todo.slug})
           self.assertTrue(self.load_casper_file(js_file='todo-item-detail-controls.js', test_label='Test the Checklist Detail....', url=url))