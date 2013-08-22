# -*- coding: UTF-8 -*-
"""
"""
from django.test import TestCase
from model_mommy import mommy

from glynt.apps.lawyer.transaction_packages import TransactionPackageBunch

from glynt.apps.lawyer.models import Lawyer


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