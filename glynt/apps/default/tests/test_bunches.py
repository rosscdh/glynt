# coding: utf-8
"""
"""
import unittest

from model_mommy import mommy

from glynt.apps.default.bunches import BaseDataBagBunch
from glynt.apps.default.bunches import ModelDataBagFieldNotDefinedException, ModelDataBagFieldDoesNotExistException


class TestBunchNoDataBagFieldError(BaseDataBagBunch):
    _model_databag_field = None


class TestBunchNoDataBagKeyError(BaseDataBagBunch):
    _model_data_key = None


class TestBunch(BaseDataBagBunch):
    _model_data_key = 'test_data_bag'


TEST_INSTANCE = mommy.make('company.Company')
TEST_INSTANCE_WITH_OTHER_DATABAG_FILED_NAME = mommy.make('client.ClientProfile')


class TestInvalidBaseDataBagBunch(unittest.TestCase):
    def test_no_databag_field_defined(self):
        self.assertRaises(TypeError, TestBunchNoDataBagFieldError)
        self.assertRaises(ModelDataBagFieldNotDefinedException, TestBunchNoDataBagFieldError, TEST_INSTANCE)

    def test_databag_field_not_defined_on_model(self):
        self.assertRaises(TypeError, TestBunchNoDataBagKeyError)
        self.assertRaises(ModelDataBagFieldDoesNotExistException, TestBunchNoDataBagKeyError, TEST_INSTANCE_WITH_OTHER_DATABAG_FILED_NAME)



class TestBaseDataBagBunch(unittest.TestCase):
    def setUp(self):
        self.TEST_INSTANCE = mommy.make('company.Company')
        self.TEST_INSTANCE.data['name'] = 'Monkies inc.'
        self.TEST_INSTANCE.data['location'] = 'Mönchengladbach'

        self.TEST_INSTANCE.save(update_fields=['data'])

        self.subject = TestBunch(instance=self.TEST_INSTANCE)

    def test_databag_property_is_present_and_dict(self):
        self.assertTrue(hasattr(self.subject, 'data_bag'))
        self.assertTrue(type(self.subject.data_bag) == dict)

    def test_databag_returns_correct_data(self):
        self.assertTrue('name' in self.subject.data_bag)
        self.assertEqual('Monkies inc.', self.subject.data_bag.get('name'))

        self.assertTrue('location' in self.subject.data_bag)
        self.assertEqual('Mönchengladbach', self.subject.data_bag.get('location'))

    def test_databag_saves_and_updates_correct_data(self):
        self.subject.save(name='Camels inc.', location='Sahara Desert')

        self.assertEqual('Camels inc.', self.subject.data_bag.get('name'))
        self.assertEqual('Sahara Desert', self.subject.data_bag.get('location'))
