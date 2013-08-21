# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from pyquery import PyQuery as pq
from .base import BaseCasperJs


class PyQueryMixin(LiveServerTestCase):
    """
    Base mixin for using PyQuery for response.content selector lookups
    https://pypi.python.org/pypi/pyquery
    """
    def setUp(self):
        self.pq = pq


class BaseLawyerCustomerProjectCaseMixin(BaseCasperJs):
    """
    Base mixin for a Setup to be used in lawyer/customer/project analysis
    https://github.com/dobarkod/django-casper/
    """
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