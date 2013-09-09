# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.test.client import Client

from model_mommy import mommy
from pyquery import PyQuery as pq
from .base import BaseCasperJs

from glynt.apps.todo import TODO_STATUS
from glynt.apps.transact.models import Transaction

import httpretty


class PyQueryMixin(LiveServerTestCase):
    """
    Base mixin for using PyQuery for response.content selector lookups
    https://pypi.python.org/pypi/pyquery
    """
    def setUp(self):
        super(PyQueryMixin, self).setUp()
        self.pq = pq


class BaseLawyerCustomerProjectCaseMixin(BaseCasperJs):
    """
    Base mixin for a Setup to be used in lawyer/customer/project analysis
    https://github.com/dobarkod/django-casper/
    """
    fixtures = ['test_cities', 'transact.json']

    @httpretty.activate
    def setUp(self):
        # mock the attachment upload
        httpretty.register_uri(httpretty.POST, "https://crocodoc.com/api/v2/document/upload",
                       body='{"success": true, "uuid": "123-test-123-uuid"}',
                       status=200,
                       content_type='text/json')

        super(BaseLawyerCustomerProjectCaseMixin, self).setUp()
        self.client = Client()

        self.password = 'password'
        self.customer_user = mommy.make('auth.User', username='customer', first_name='Customer', last_name='A', email='customer+test@lawpal.com')
        self.customer_user.set_password(self.password)
        self.customer_user.save()

        self.company = mommy.make('company.Company', customers=(self.customer_user,))

        customer_profile = self.customer_user.profile
        customer_profile.profile_data['user_class_name'] = 'customer'
        customer_profile.profile_data['is_customer'] = True
        customer_profile.save()

        self.customer = mommy.make('customer.Customer', user=self.customer_user)

        self.lawyer_user = mommy.make('auth.User', username='lawyer', first_name='Lawyer', last_name='A', email='lawyer+test@lawpal.com')
        self.lawyer_user.set_password(self.password)
        self.lawyer_user.save()

        lawyer_profile = self.lawyer_user.profile
        lawyer_profile.profile_data['user_class_name'] = 'lawyer'
        lawyer_profile.profile_data['is_lawyer'] = True
        lawyer_profile.save()

        self.lawyer = mommy.make('lawyer.Lawyer', user=self.lawyer_user)
        
        self.project = mommy.make('project.Project', customer=self.customer, lawyers=(self.lawyer,), transactions=(Transaction.objects.get(slug='CS'), Transaction.objects.get(slug='SF'),))

        # set the join to status engaged
        self.project_lawyer_join = self.project.projectlawyer_set.all()[0]
        self.project_lawyer_join.status = self.project_lawyer_join.LAWYER_STATUS.assigned
        self.project_lawyer_join.save(update_fields=['status'])


        self.todo = mommy.make('todo.ToDo', status=TODO_STATUS.open, project=self.project, user=self.lawyer_user, category='General', name="My Todo")
        self.attachment = mommy.make('todo.Attachment', project=self.project, todo=self.todo, uploaded_by=self.customer_user)