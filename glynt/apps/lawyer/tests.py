"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django import template
from django.test.utils import override_settings

import unittest


class TestStub(unittest.TestCase):
    def setUp(self):
        pass