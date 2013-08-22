# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin
from glynt.apps.project.models import Project, ProjectLawyer

import os

#from nose.tools import set_trace; set_trace()
class DashboardLawyerTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
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


class ChecklistLawyerTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.dirname(__file__)

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

        # Test we have the required item attribs
        required_attribs = ['data-edit_label', 'data-status']
        for e in c('tr.item'):
            elem = self.pq(e)

            for a in required_attribs:
                self.assertTrue(elem.attr(a))

            # test we have an edit link
            self.assertTrue(len(elem.find('a.item-edit')) == 1)
            # is it modal and does it have the correct attribs
            edit = self.pq(elem.find('a.item-edit'))
            self.assertTrue(edit.attr('data-toggle') == 'modal') # is a modal link
            self.assertTrue(edit.attr('data-target') == '#modal-checklist-item') # and the modal target is correct
            
            # test we have 1 delete link
            self.assertTrue(len(elem.find('a.item-delete')) == 1)

    def test_lawyer_dashboard_js(self):
        self.client.login(username=self.lawyer_user.username, password=self.password)
        url = reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid})
        self.assertTrue(self.load_casper_file(js_file='checklist-lawyer.js', test_label='Test the Checklist View for a Lawyer', url=url))
        # from nose.tools import set_trace; set_trace()