"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django import template
from django.test.utils import override_settings

import unittest


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TestHumaniseNumber(unittest.TestCase):
    def setUp(self):
        self.obj = '500k'
        self.context = {
            'big_number': 500000
        }

    def render_template(self, *args, **kwargs):
        context = kwargs.get('context', {})
        t = template.Template(''.join(args))
        c = template.Context(context)
        return t.render(c)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_humanise(self):
        result = self.render_template(
            '{% load lawyer_profile_tags %}'
            ,'{% humanise_number num=big_number %}'
            , context=self.context
        )

        self.assertEqual(result, self.obj)