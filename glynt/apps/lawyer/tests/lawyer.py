# -*- coding: UTF-8 -*-
"""
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin

from glynt.apps.lawyer.transaction_packages import TransactionPackageBunch

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.project.models import Project


class LawyerNavDropDownTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    """
    Test the nav dropdown contains projects based on VisibleProjectService
    """
    def test_assigned_lawyer_sees_projects(self):
        """
        If a lawyer has assigned projects then we should see them in the request.projects
        """
        self.client.login(username=self.lawyer_user.username, password=self.password)
        resp = self.client.get(reverse('dashboard:overview'))

        self.assertTrue(len(resp.context['request'].projects) == 1)
        self.assertTrue(resp.context['request'].projects == [self.project])

        self.assertTrue(type(resp.context['request'].project) == Project)
        self.assertTrue(resp.context['request'].project == self.project)

        c = self.pq(resp.content)
        self.assertEqual(len(c('ul#project-set')), 1) # we see navigation project-set list
        self.assertEqual(len(c('ul#project-set li.dropdown')), 1) # we see navigation project-set list

    def test_unassigned_lawyer_sees_no_projects(self):
        """
        If a lawyer has no assigned projects then nothing shoudl show in the request.projects
        """
        unassigned_lawyer_user = self.make_user(username='unassigned_lawyer', first_name='UnAssigned', last_name='Lawyer', email='unassigned_lawyer+test@lawpal.com')
        unassigned_lawyer = mommy.make('lawyer.Lawyer', user=unassigned_lawyer_user)

        self.client.login(username=unassigned_lawyer.user.username, password=self.password)
        resp = self.client.get(reverse('public:homepage'))

        self.assertTrue(resp.context['request'].projects == [])
        self.assertTrue(resp.context['request'].project is None)

        c = self.pq(resp.content)
        self.assertEqual(len(c('ul#project-set')), 0) # we have 0 navigation project-set list


class LawyerModelMethodsTest(TestCase):
    def setUp(self):
        self.user = mommy.make('auth.User', first_name='Monkey', last_name='Boy')
        self.lawyer = mommy.make('lawyer.Lawyer', user=self.user)
        self.firm = mommy.make('firm.Firm', lawyers=[self.lawyer])

        self.no_firm_lawyer = mommy.make('lawyer.Lawyer')

    def test_primary_firm(self):
        self.assertTrue(self.lawyer.primary_firm is not None)
        self.assertTrue(self.no_firm_lawyer.primary_firm is None)

    def test_firm_name(self):
        self.assertTrue(self.lawyer.firm_name is not None)
        self.assertTrue(self.no_firm_lawyer.firm_name is None)

    def test_position(self):
        self.assertTrue(self.lawyer.position is not None)
        self.assertEqual(self.lawyer.position, 'Associate')
        self.assertEqual(self.lawyer.position, Lawyer.LAWYER_ROLES.get_desc_by_value(self.lawyer.role))

    def test_username(self):
        self.assertTrue(self.lawyer.username is not None)

    def test_full_name(self):
        """
        if no full_name is specified in the data_bag then retrieve it from the user object
        """
        self.assertTrue(self.lawyer.full_name is not None)
        self.assertEqual(self.lawyer.full_name, self.user.get_full_name())

        """
        If we have the data in the data_bag then retrieve that
        """
        self.lawyer.data['first_name'] = '  Lewis '
        self.lawyer.data['last_name'] = 'Carroll  '

        self.assertEqual(self.lawyer.full_name, 'Lewis Carroll')

    def test_profile_status(self):
        self.assertEqual(self.lawyer.profile_status, 'pending activation and will appear live shortly.')

        self.lawyer.is_active = True
        self.assertEqual(self.lawyer.profile_status, 'live')

    def test_default_fee_packages(self):
        self.assertEqual(type(self.lawyer.fee_packages), TransactionPackageBunch)

    def test_default_companies_advised(self):
        self.assertEqual(type(self.lawyer.companies_advised), list)

    def test_default_geo_loc(self):
        self.assertEqual(type(self.lawyer.geo_loc), type(None))