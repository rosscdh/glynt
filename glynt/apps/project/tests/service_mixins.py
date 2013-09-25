# -*- coding: UTF-8 -*-
from django.utils import unittest

from glynt.apps.project.services.mixins import JavascriptRegionCloneMixin
from glynt.apps.project.services.mixins.region_clone import RE_FIND_END_NUMERAL

import json
import re


class TestJavascriptRegionCloneMixin(unittest.TestCase):
    def setUp(self):
        self.subject = JavascriptRegionCloneMixin()
        self.region_clone_key = 'founders'
        self.test_items = json.loads('{"founders": {                \
                                        "founder_email_2": {        \
                                          "id": "founder_email_2",  \
                                          "val": "yael@lawpal.com", \
                                          "name": "founder_email_2" \
                                        },                          \
                                        "founder_email_1": {        \
                                          "id": "founder_email_1",  \
                                          "val": "alex@lawpal.com", \
                                          "name": "founder_email_1" \
                                        },                          \
                                        "founder_name": {           \
                                          "id": "founder_name",     \
                                          "val": "Ross Crawford",   \
                                          "name": "founder_name"    \
                                        },                          \
                                        "founder_name_2": {         \
                                          "id": "founder_name_2",   \
                                          "val": "Yael",            \
                                          "name": "founder_name_2"  \
                                        },                          \
                                        "founder_name_1": {         \
                                          "id": "founder_name_1",   \
                                          "val": "Alex Halliday",   \
                                          "name": "founder_name_1"  \
                                        },                          \
                                        "founder_email": {          \
                                          "id": "founder_email",    \
                                          "val": "ross@lawpal.com", \
                                          "name": "founder_email" } \
                                        }                           \
                                    }')

    def test_parse_repeater_dict(self):
        """
        test the primary entry point
        """
        res = self.subject.parse_repeater_dict(items=self.test_items.get(self.region_clone_key))
        self.assertEqual(type(res), list)  # we get a list returned
        self.assertEqual(len(res), 3)  # of 3 objects

        for i in res:
            self.assertEqual(type(i), dict)  # the items are dicts
            self.assertEqual(len(i.keys()), 2) # we should have 2 keys per object: 'founder_email', 'founder_name'
            # ensure that we only have the corrected item keys
            self.assertEqual(i.keys(), ['founder_email', 'founder_name'])
            # ensure that we DONT have the original sequence keys present
            self.assertTrue(['founder_name_1', 'founder_name_2', 'founder_email_1', 'founder_email_2'] not in i.keys())

    def test_extract_repeater_values(self):
        pass


class TestRegexp(unittest.TestCase):
    def test_RE_FIND_END_NUMERAL(self):
        self.assertTrue(isinstance(RE_FIND_END_NUMERAL, re._pattern_type))
        self.assertEqual(RE_FIND_END_NUMERAL.pattern, '_(\\d+)$')