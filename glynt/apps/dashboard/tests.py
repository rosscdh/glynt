# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from glynt.casper import BaseLawyerCustomerProjectCaseMixin
from glynt.apps.project.models import Project, ProjectLawyer

import os

#from nose.tools import set_trace; set_trace()
class DashboardCasperJsTest(PyQueryMixin, BaseLawyerCustomerProjectCaseMixin):
    test_path = os.path.dirname(__file__)

    def test_dashboard_lawyer_access_anonymous(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 302)

    def test_dashboard_access(self):
        self.client.login(username=self.lawyer_user.username, password=self.password)

        resp = self.client.get('/dashboard/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('project' in resp.context)
        self.assertEqual(type(resp.context['project']), Project)

        self.assertTrue('counts' in resp.context)
        self.assertEqual(type(resp.context['counts']), dict)

    def test_lawyer_dashboard_js(self):
        """
        """
        pl_join = ProjectLawyer.objects.filter(project=self.project, lawyer=self.lawyer)

        self.client.login(username=self.lawyer_user.username, password=self.password)
        self.assertTrue(self.load_casper_file(js_file='dashboard.js', test_label='Test the Dashboard View for a Lawyer'))
        # from nose.tools import set_trace; set_trace()