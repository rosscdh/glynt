# coding: utf-8
"""
Test the todo bunches
"""

import mocktest 
from glynt.apps.transact.bunches import IncorporationBunch


class IncorporationBunchTest(mocktest.TestCase):
    """ Ensure the IncorporationBunch is setup correctly """
    expected_subject_slug_and_names = [('general', 'General Questions'),
                                ('qualification', 'Qualification to do business in other states or countries'),
                                ('founders_docs', 'Founders Documents'),
                                ('option_plan', 'Option Plan'),
                                ('options', 'Option Issuance'),
                                ('directors_and_officers', 'Directors and Officers'),
                                ('employment_docs', 'Employment Documents'),
                                ('consultant_docs', 'Consultant Documents'),
                                ('intellectual_property', 'Intellectual Property'),
                                ('misc', 'Miscellaneous'),
                            ]

    def setUp(self):
        self.subject = IncorporationBunch()


    def test_general_properties(self):
        self.assertTrue(hasattr(self.subject, 'name'))
        self.assertEqual('Incorporation', self.subject.name)

        self.assertTrue(hasattr(self.subject, 'transaction_slug'))
        self.assertEqual('incorporation', self.subject.transaction_slug)

        self.assertTrue(hasattr(self.subject, 'todos'))
        self.assertEqual(type(self.subject.todos), tuple)

    def test_todo_keys(self):
        slugs = []
        names = []
        for slug, name, todos in self.subject.todos:
            slugs.append(slug)
            slugs.append(name)
            self.assertEqual(type(todos), tuple)

        for slug, name in self.expected_subject_slug_and_names:
            self.assertEqual(True, slug in slugs)
            self.assertEqual(True, name in names)
            print name
            print slug

        
