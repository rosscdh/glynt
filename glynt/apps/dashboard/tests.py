# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test.client import Client
from model_mommy import mommy

from glynt.casper import BaseCasperJs
from glynt.apps.project.models import Project, ProjectLawyer

import os

#from nose.tools import set_trace; set_trace()
class DashboardCasperJsTest(BaseCasperJs):
    test_path = os.path.dirname(__file__)

    fixtures = ['cities_light.json']

    def setUp(self):
        self.client = Client()

        self.password = 'password'
        self.customer_user = mommy.make('auth.User', username='customer', first_name='Customer', last_name='A')
        self.customer_user.set_password(self.password)
        self.customer_user.save()

        self.company = mommy.make('company.Company', customers=(self.customer_user,))

        customer_profile = self.customer_user.profile
        customer_profile.profile_data['user_class_name'] = 'customer'
        customer_profile.profile_data['is_customer'] = True
        customer_profile.save()

        self.customer = mommy.make('customer.Customer', user=self.customer_user)

        self.lawyer_user = mommy.make('auth.User', username='lawyer', first_name='Lawyer', last_name='A')
        self.lawyer_user.set_password(self.password)
        self.lawyer_user.save()

        lawyer_profile = self.lawyer_user.profile
        lawyer_profile.profile_data['user_class_name'] = 'lawyer'
        lawyer_profile.profile_data['is_lawyer'] = True
        lawyer_profile.save()

        self.lawyer = mommy.make('lawyer.Lawyer', user=self.lawyer_user)

        self.assertTrue(self.lawyer_user.profile.is_lawyer)
        self.assertTrue(self.customer_user.profile.is_customer)
        
        self.project = mommy.make('project.Project', customer=self.customer, lawyers=(self.lawyer,))

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