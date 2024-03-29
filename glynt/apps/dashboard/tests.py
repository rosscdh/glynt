# -*- coding: utf-8 -*-
"""
@TODO set test descriptor
"""
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin, for_all_methods, glynt_mock_http_requests
from glynt.apps.project.models import Project, ProjectLawyer

from model_mommy import mommy

import os


@for_all_methods(glynt_mock_http_requests)
class DashboardLawyerTest(BaseLawyerCustomerProjectCaseMixin):
    def setUp(self):
        super(DashboardLawyerTest, self).setUp()

        self.url = reverse('dashboard:overview')

    def test_dashboard_lawyer_access_anonymous(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_dashboard_access_js(self):
        self.client.login(username=self.lawyer_user.username, password=self.password)

        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)

        self.assertTrue('project' in resp.context_data)
        self.assertEqual(type(resp.context_data['project']), Project)

        self.assertTrue('counts' in resp.context_data)
        self.assertEqual(type(resp.context_data['counts']), dict)

        self.assertTrue(self.load_casper_file(js_file='dashboard_access.js', test_label='Test the Dashboard Access for a Lawyer', url=self.url))

    def test_lawyer_dashboard_js(self):
        """
        """
        ProjectLawyer.objects.filter(project=self.project, lawyer=self.lawyer)

        self.client.login(username=self.lawyer_user.username, password=self.password)

        self.project_lawyer_join.status = self.project_lawyer_join._LAWYER_STATUS.potential
        self.project_lawyer_join.save(update_fields=['status'])

        self.assertTrue(self.load_casper_file(js_file='dashboard.js', test_label='Test the Dashboard View for a Lawyer', url=self.url))


@for_all_methods(glynt_mock_http_requests)
class ChecklistLawyerTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    def test_checklist_access_anonymous(self):
        resp = self.client.get(reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid}))
        self.assertEqual(resp.status_code, 302)

    def test_checklist_lawyer_access(self):
        self.client.login(username=self.lawyer_user.username, password=self.password)

        resp = self.client.get(reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid}))
        self.assertEqual(resp.status_code, 200)

        c = self.pq(resp.content)

        self.assertEqual(len(c('ul#checklist-categories')), 1) # we have 1 checklist-categories ul
        self.assertTrue(len(c('ul#checklist-categories li')) > 0) # we have 1 or more checklist-categories ul li elements
        self.assertTrue(len(c('button.create-item')) > 0) # we have 1 or more add item buttons

        self.assertTrue(len(c('tr.item')) >= 1) # we have 1 or more add item buttons

    def test_lawyer_dashboard_js(self):
        self.client.login(username=self.lawyer_user.username, password=self.password)

        # Create feedback request for testing of assigned to indicator on checklist
        mommy.make('todo.FeedbackRequest', attachment=self.attachment, assigned_by=self.customer_user, assigned_to=(self.lawyer_user,), comment='What are your thoughts on this test file with ümlauts')

        url = reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='checklist-lawyer.js', test_label='Test the Checklist View for a Lawyer', url=url))
        self.assertTrue(self.load_casper_file(js_file='checklist-lawyer-categories.js', test_label='Test the Checklist View ability to move Categories', url=url))
        self.assertTrue(self.load_casper_file(js_file='checklist-lawyer-attachments.js', test_label='Test the Checklist View attachment counts', url=url))
        self.assertTrue(self.load_casper_file(js_file='checklist-lawyer-pusher.js', test_label='Test the Checklist View pusher events', url=url))

