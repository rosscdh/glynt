"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django import template
from django.test.utils import override_settings

import unittest


class TestHumaniseNumber(unittest.TestCase):
    def setUp(self):
        self.expected_k_result = '500k'

        self.context = {
            'big_number': 500000,
            'no_strings_allowed' : 'lawpal rulez',
            'no_unicode_allowed' : u"\xc5",
            'no_empty_strings_allowed' : '',
            'no_neg_integers_allowed' : '-200000',
            'no_floating_allowed' : '200.403424230'
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

        self.assertEqual(result, self.expected_k_result)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_humanise_converts_strings_to_zero(self):
        result = self.render_template(
            '{% load lawyer_profile_tags %}'
            ,'{% humanise_number num=no_strings_allowed %}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_unicode_to_zero(self):
        result = self.render_template(
            '{% load lawyer_profile_tags %}'
            ,'{% humanise_number num=no_unicode_allowed %}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_empty_string_to_zero(self):
        result = self.render_template(
            '{% load lawyer_profile_tags %}'
            ,'{% humanise_number num=no_empty_strings_allowed %}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_negative_integers_to_zero(self):
        result = self.render_template(
            '{% load lawyer_profile_tags %}'
            ,'{% humanise_number num=no_neg_integers_allowed %}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_floating_to_zero(self):
        result = self.render_template(
            '{% load lawyer_profile_tags %}'
            ,'{% humanise_number num=no_floating_allowed %}'
            , context=self.context
        )

        self.assertEqual(result, '0')