# coding: utf-8
"""
Test the todo bunches
"""
import factory
import mocktest 
from glynt.apps.transact.models import Transaction
from glynt.apps.transact.bunches import BaseToDoBunch, IncorporationBunch


class TransactionFactory(factory.Factory):
    FACTORY_FOR = Transaction


class BaseToDoBunchAttribsTest(mocktest.TestCase):
    """ Test the base class that contains the core repeater and structure """
    def setUp(self):
        self.transaction = TransactionFactory.build()
        self.subject = BaseToDoBunch()

    def test_general_properties(self):
        self.assertTrue(hasattr(self.subject, 'name'))
        self.assertTrue(hasattr(self.subject, 'transaction_slug'))
        self.assertTrue(hasattr(self.subject, 'todos'))

    def test_attribute_types(self):
        self.assertEqual(type(self.subject.todos), list) # to allow for appending of todos


class BaseToDoBunchMethodsTest(mocktest.TestCase):
    def setUp(self):
        self.transaction = TransactionFactory.build()
        self.subject = BaseToDoBunch()

    def test_todo_block(self):
        pass
    def test_generate_repeaters(self):
        pass
    def test_update_todo_context(self):
        pass


class IncorporationBunchTest(BaseToDoBunchAttribsTest):
    """ Ensure the IncorporationBunch is setup correctly """
    expected_repeaters = [('customer_docs', 'customer'),
                            ('options', 'options'),
                            ('directors_and_officers', 'director'),
                            ('employment_docs', 'employee'),
                        ]
    expected_subject_slug_and_names = [('general', 'General Questions'),
                                ('qualification', 'Qualification to do business in other states or countries'),
                                ('customer_docs', 'Customers Documents'),
                                ('option_plan', 'Option Plan'),
                                ('options', 'Option Issuance'),
                                ('directors_and_officers', 'Directors and Officers'),
                                ('employment_docs', 'Employment Documents'),
                                ('consultant_docs', 'Consultant Documents'),
                                ('intellectual_property', 'Intellectual Property'),
                                ('misc', 'Miscellaneous'),
                            ]

    def setUp(self):
        self.transaction = TransactionFactory.build()
        self.subject = IncorporationBunch(transaction=self.transaction)

    def test_properties(self):
        self.assertEqual('Incorporation', self.subject.name)
        self.assertEqual('incorporation', self.subject.transaction_slug)

    def test_repeaters(self):
        slugs = []
        names = []
        for slug, name in self.subject.repeaters:
            slugs.append(slug)
            names.append(name)

        for slug, name in self.expected_repeaters:
            self.assertTrue(slug in slugs)
            self.assertTrue(name in names)

    def test_todo_keys(self):
        slugs = []
        names = []
        for slug, name, todos in self.subject.todos:
            slugs.append(slug)
            names.append(name)
            # test todos is a tuple
            self.assertEqual(type(todos), tuple)

        # test expected name and slug are in the set
        for slug, name in self.expected_subject_slug_and_names:
            self.assertTrue(slug in slugs)
            self.assertTrue(name in names)

        
