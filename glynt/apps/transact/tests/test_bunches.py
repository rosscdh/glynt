# coding: utf-8
"""
Test the todo bunches
"""
import factory
import unittest

from collections import OrderedDict

from glynt.apps.transact.models import Transaction
from glynt.apps.todo.bunches import BaseToDoBunch
from glynt.apps.transact.bunches import IncorporationBunch

#from nose.tools import set_trace; set_trace()

class TransactionFactory(factory.Factory):
    FACTORY_FOR = Transaction


class BaseToDoBunchAttribsTest(unittest.TestCase):
    """ Test the base class that contains the core repeater and structure """
    def setUp(self):
        self.transaction = TransactionFactory.build()
        self.subject = BaseToDoBunch()

    def test_general_properties(self):
        self.assertTrue(hasattr(self.subject, 'name'))
        self.assertTrue(hasattr(self.subject, 'template'))


class IncorporationBunchTest(BaseToDoBunchAttribsTest):
    """ Ensure the IncorporationBunch is setup correctly """
    expected_subject_names = ['General',
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
        #self.transaction = TransactionFactory.build()
        self.subject = IncorporationBunch()

    def test_properties(self):
        """ name is set to the base class name """
        self.assertEqual('Incorporation', self.subject.name)

    def test_todos_are_set(self):
        self.assertTrue(type(self.subject.todos) == OrderedDict)
        todo_keys = self.subject.todos.keys()
        for e in self.expected_subject_names:
            #print '"%s" in %s' % (e, todo_keys)
            self.assertEqual(True, e.strip() in todo_keys)

    def test_repeaters_are_set_and_simple_types(self):
        for name, value_dict in self.subject.todos.iteritems():

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


