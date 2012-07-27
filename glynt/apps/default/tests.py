"""
Test the default app views
"""
from django.test.client import Client
from django.test import TestCase

from django.core.urlresolvers import reverse

login_required_urls = [
		reverse('glynt:default'), 
		]


class DefaultAppTest(TestCase):
	def setUp(self):
		self.client = Client()
