# -*- coding: UTF-8 -*-
"""
Test the todo bunches
"""
from glynt.apps.todo.bunches import BaseToDoBunch
from glynt.apps.transact.bunches import IncorporationBunch, SeedFundingEquityRoundBunch, SeedFundingConvertibleNoteRoundBunch

from collections import OrderedDict
from model_mommy import mommy

import factory
from django.utils import unittest


class BaseToDoBunchAttribs(unittest.TestCase):
    """ Test the base class that contains the core repeater and structure """
    expected_subject_names = []
    expected_repeaters = []

    def setUp(self):
        self.subject = BaseToDoBunch()

    def test_general_properties(self):
        self.assertTrue(hasattr(self.subject, 'name'))
        self.assertTrue(hasattr(self.subject, 'template'))

    def test_todos_are_set(self):
        self.assertTrue(type(self.subject.todos) == OrderedDict)

        todo_keys = self.subject.todos.keys()

        for e in self.expected_subject_names:
            #print '"%s" in %s' % (e, todo_keys)
            self.assertEqual(True, e.strip() in todo_keys)

    def test_repeaters_are_set_and_simple_types(self):
        #print("\nClass: {cls} in transaction_name: {tx_name}".format(cls=self.__class__.__name__, tx_name=self.subject.name))

        for name, value_dict in self.subject.todos.iteritems():
            #print("\ntest name: {name} - expected:\n{expected}\n".format(name=name, expected=self.expected_subject_names))

            self.assertTrue(type(name) == str)
            self.assertTrue(name in self.expected_subject_names)

            if name in self.expected_repeaters:
                self.assertTrue(value_dict.type == 'repeater')
            else:
                self.assertTrue(value_dict.type == 'simple')

    def test_checklist_items_are_set(self):
        for name, value_dict in self.subject.todos.iteritems():

            self.assertTrue(type(value_dict.checklist) == list)

            self.assertTrue(len(value_dict.checklist) > 0)

            for todo in value_dict.checklist:
                self.assertTrue(hasattr(todo, 'name'))


class IncorporationBunchTest(BaseToDoBunchAttribs):
    """
    Ensure the IncorporationBunch is setup correctly
    """
    expected_subject_names = ['Transaction Setup',
                                'General',
                                'Qualification to do business',
                                'Founders Documents',
                                'Option Plan',
                                'Option Holders',
                                'Option Holders - International',
                                'Directors & Officers',
                                'Employment Documents',
                                'Consultant Documents',
                                'Intellectual Property',
                                'Miscellaneous',
                            ]
    expected_repeaters = [  'Founders Documents',
                            'Option Holders',
                            'Directors & Officers',
                            'Employment Documents',
                            'Consultant Documents',
                         ]

    def setUp(self):
        self.subject = IncorporationBunch()

    def test_properties(self):
        """ name is set to the base class name """
        self.assertEqual('Incorporation', self.subject.name)


class SeedFundingConvertibleNoteRoundBunchTest(BaseToDoBunchAttribs):
    """
    Ensure the SeedFundingConvertibleNoteRoundBunch is setup correctly
    """
    expected_subject_names = ['Transaction Setup',
                              'Note Purchase Agreement',
                              'Corporate Approvals',
                              'Due Diligence',
                              'Closing Documents']
    expected_repeaters = []

    def setUp(self):
        self.subject = SeedFundingConvertibleNoteRoundBunch()

    def test_properties(self):
        """ name is set to the base class name """
        self.assertEqual('Seed Financing : Convertible Note Round', self.subject.name)


class SeedFundingEquityRoundBunchTest(BaseToDoBunchAttribs):
    """
    Ensure the SeedFundingEquityRoundBunch is setup correctly
    """
    expected_subject_names = ['General']
    expected_repeaters = []

    def setUp(self):
        self.subject = SeedFundingEquityRoundBunch()

    def test_properties(self):
        """ name is set to the base class name """
        self.assertEqual('Seed Financing : Equity Round', self.subject.name)
