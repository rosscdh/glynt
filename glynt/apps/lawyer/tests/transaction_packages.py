# -*- coding: UTF-8 -*-
"""
"""

from django.test import TestCase
from django import template
from django.test.utils import override_settings

import unittest
import json

from glynt.apps.lawyer.transaction_packages import TransactionPackageBunch
from glynt.apps.lawyer.transaction_packages import TRANSACTION_PACKAGES


class TestTransactionPackageService(unittest.TestCase):
    def setUp(self):
        self.service_class = TransactionPackageBunch
        # What the data currently looks like in the Lawyer.data model
        self.input = {
                          "seed_fee_cap_available": True,
                          "seed_deferred_fees_available": False,
                          "seed_fixed_fees_available": True,
                          "seed_financing_amount_min": 0,
                          "seed_financing_amount_max": 0,

                          "inc_fee_cap_available": False,
                          "inc_deferred_fees_available": False,
                          "inc_fixed_fees_available": False,
                          "incorporation_min": 0,
                          "incorporation_max": 0, 

                          "optional_funding": "Test Optional Title",
                          "optional_fee_cap_available": False,
                          "optional_deferred_fees_available": False,
                          "optional_fixed_fees_available": False,
                          "optional_min": 0,
                          "optional_max": 0,

                          "optional_funding2": "Test Optional Title 2",
                          "optional_fee_cap_available2": False,
                          "optional_deferred_fees_available2": False,
                          "optional_fixed_fees_available2": False,
                          "optional_min2": 0,
                          "optional_max2": 0,

                          "optional_funding3": "Test Optional Title 3",
                          "optional_fee_cap_available3": False,
                          "optional_deferred_fees_available3": False,
                          "optional_fixed_fees_available3": False,
                          "optional_min3": 0,
                          "optional_max3": 0,
                        }
        # How we would want it to look
        self.expected = {
            "seed_financing_amount": {
                          "title": "Seed Financing",
                          "fee_cap_available": True,
                          "deferred_fees_available": False,
                          "fixed_fees_available": True,
                          "key": 'seed_financing_amount',
                          "max": 0,
                          "min": 0,
            },
            "incorporation": {
                          "title": "Incorporation",
                          "fee_cap_available": False,
                          "deferred_fees_available": False,
                          "fixed_fees_available": False,
                          "key": 'incorporation',
                          "max": 0,
                          "min": 0,
            },
            "optional": {
                          "title": "Test Optional Title",
                          "fee_cap_available": False,
                          "deferred_fees_available": False,
                          "fixed_fees_available": False,
                          "key": 'optional',
                          "max": 0,
                          "min": 0,
            },
            "optional2": {
                          "title": "Test Optional Title 2",
                          "fee_cap_available": False,
                          "deferred_fees_available": False,
                          "fixed_fees_available": False,
                          "key": 'optional',
                          "max": 0,
                          "min": 0,
            },
            "optional3": {
                          "title": "Test Optional Title 3",
                          "fee_cap_available": False,
                          "deferred_fees_available": False,
                          "fixed_fees_available": False,
                          "key": 'optional',
                          "max": 0,
                          "min": 0,
            },
        }
    def test_constants(self):
        assert TRANSACTION_PACKAGES == (('seed_financing_amount','seed','Seed Financing'),
                        ('incorporation','inc','Incorporation'),
                        ('optional',1,'optional_funding'),
                        ('optional',2,'optional_funding'),
                        ('optional',3,'optional_funding'),)

    def keys_are_in_subject(self,subject):
        expected_keys = self.expected.keys()
        expected_sub_item_keys = self.expected.get('seed_financing_amount').keys()
        expected_sub_item_keys.sort()  # sort the array for comparison

        # test each expected key is in the packages keys
        self.assertEqual(expected_keys, subject.packages.keys())

        # Ensure that all the sub packages have the same set of keys
        for key,val_dic in subject.packages.items():
            value_item_keys = val_dic.keys()
            value_item_keys.sort() # sort the array for comparison

            # assert that the sub package contains all of the keys required
            self.assertEqual(value_item_keys, expected_sub_item_keys)

    def test_package_keys_are_present_in_empty_data(self):
        subject = self.service_class(data={})
        self.keys_are_in_subject(subject=subject)

    def test_package_keys_are_present_in_invalid_data(self):
        data = {
          "optional_funding": "I sell Murkey Data",
          "optional_fee_cap_available": 'thisIs_A_totally_23o value',
          "optional_deferred_fees_available": 'thisIs_A_totally_23o value',
          "optional_fixed_fees_available": 'thisIs_A_totally_23o value',
          "optional_min": 'thisIs_A_totally_23o value',
          "optional_max": 'thisIs_A_totally_23o value',
        }
        subject = self.service_class(data=data)
        self.keys_are_in_subject(subject=subject)

        result_items = subject.packages.get('optional')

        self.assertEqual(result_items.get('title'), 'I sell Murkey Data')
        self.assertEqual(result_items.get('fee_cap_available'), False)
        self.assertEqual(result_items.get('deferred_fees_available'), False)
        self.assertEqual(result_items.get('fixed_fees_available'), False)
        self.assertEqual(result_items.get('min'), 0)
        self.assertEqual(result_items.get('max'), 0)

    def test_package_keys_are_present(self):
        subject = self.service_class(data=self.input.copy())
        self.keys_are_in_subject(subject=subject)

    def test_representations(self):
        subject = self.service_class(data=self.input.copy())
        assert type(subject.items()) == list # items returns a list of bunch objects
        assert type(subject.packages) == dict # the packages are stored as a key->value hash
        
    def test_optional_item(self):
        data = {
          "optional_funding": "I Sell Monkies Cheap",
          "optional_fee_cap_available": True,
          "optional_deferred_fees_available": False,
          "optional_fixed_fees_available": True,
          "optional_min": 0,
          "optional_max": 2500,
        }

        subject = self.service_class(data=data)
        self.keys_are_in_subject(subject=subject)

        result_items = subject.packages.get('optional')

        self.assertEqual(result_items.get('title'), 'I Sell Monkies Cheap')
        self.assertEqual(result_items.get('fee_cap_available'), True)
        self.assertEqual(result_items.get('deferred_fees_available'), False)
        self.assertEqual(result_items.get('fixed_fees_available'), True)
        self.assertEqual(result_items.get('min'), 0)
        self.assertEqual(result_items.get('max'), 2500)

    def test_optional_increment_item(self):
        """ Loop over optionals 2 and 3 and ensure that we can access their set values """
        for i in range(2,3):

            data = {
              "optional_funding%d"%i: "I Sell %d Monkies Cheap"%i,
              "optional_fee_cap_available%d"%i: True,
              "optional_deferred_fees_available%d"%i: False,
              "optional_fixed_fees_available%d"%i: True,
              "optional_min%d"%i: 0,
              "optional_max%d"%i: 2500,
            }

            subject = self.service_class(data=data)
            self.keys_are_in_subject(subject=subject)

            result_items = subject.packages.get('optional%d'%i)

            self.assertEqual(result_items.get('title'), 'I Sell %d Monkies Cheap'%i)
            self.assertEqual(result_items.get('fee_cap_available'), True)
            self.assertEqual(result_items.get('deferred_fees_available'), False)
            self.assertEqual(result_items.get('fixed_fees_available'), True)
            self.assertEqual(result_items.get('min'), 0)
            self.assertEqual(result_items.get('max'), 2500)
