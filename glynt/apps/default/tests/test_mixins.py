# coding: utf-8
"""
Test the Various Mixins for this app
"""
from django import forms
import unittest

from model_mommy import mommy

from glynt.apps.default.mixins import AngularAttribsFormFieldsMixin


"""
Test that the AngularAttribsFormFieldsMixin adds the 2 required
data attributes specified by Lee
"""

class TestForm(AngularAttribsFormFieldsMixin, forms.Form):
    """
    Test form for our local testing
    """
    name_with_initial = forms.CharField(initial='We have Initial')
    name_without_initial = forms.CharField()


class TestAngularAttribsFormFieldsMixin(unittest.TestCase):
    """
    Test for default initial values
    """
    def setUp(self):
        self.subject = TestForm()
        self.html = str(self.subject)

    def test_angular_added_to_name_with_initial(self):
        self.assertIn('data-ng-init="We have Initial"', self.html)
        self.assertIn('data-ng-model="name_with_initial"', self.html)

    def test_angular_added_to_name_without_initial(self):
        self.assertIn('data-ng-init=""', self.html)
        self.assertIn('data-ng-model="name_without_initial"', self.html)


class TestAngularAttribsFormFieldsMixin_Initialized(unittest.TestCase):
    """
    Test for specified initial values
    """
    def setUp(self):
        self.subject = TestForm(initial={'name_with_initial': 'We have a different Initial Value now'})
        self.html = str(self.subject)

    def test_angular_added_to_name_with_initial(self):
        self.assertIn('data-ng-init="We have a different Initial Value now"', self.html)
        self.assertIn('data-ng-model="name_with_initial"', self.html)

    def test_angular_added_to_name_without_initial(self):
        self.assertIn('data-ng-init=""', self.html)
        self.assertIn('data-ng-model="name_without_initial"', self.html)