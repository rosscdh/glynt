# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from glynt.tests import TemplateRendererMixin

from BeautifulSoup import BeautifulSoup

from django.contrib.auth.models import User
from glynt.apps.factories import UserFactory, LoggedOutUserFactory


class TestContactUsForm(LiveServerTestCase, TemplateRendererMixin):
    fixtures = ['test_cities']

    def setUp(self):
        self.client = Client()
        self.contact_us_url = reverse('public:contact_us')
        self.user = User.objects.create_user('test', 'test@lawpal.com', 'test')
        self.user.first_name = 'Bob'
        self.user.last_name = 'McKelly'
        self.user.save(update_fields=['first_name', 'last_name'])

        self.context = {
            'user': self.user
        }

        self.loggedout_user = LoggedOutUserFactory.create()
        self.loggedout_context = {
            'user': self.loggedout_user
        }

    def test_presence_loggedin(self):
        """ when not logged in the user should not see the email input
        And their name should be present """
        logged_in = self.client.login(username=self.user.username, password='test')
        self.assertTrue(logged_in)
        self.assertIn('_auth_user_id', self.client.session)

        result = self.client.get(self.contact_us_url)

        soup = BeautifulSoup(result.content)

        nameElement = soup.findAll('input', id="id_name") # text
        hiddenEmailElement = soup.findAll('input', id="id_email", type="hidden") # hidden input

        self.assertTrue(len(hiddenEmailElement) == 1)
        self.assertTrue(hiddenEmailElement[0]['value'] == self.user.email)

        self.assertTrue(len(nameElement) == 1)
        self.assertTrue(nameElement[0]['value'] == self.user.get_full_name())
        
        

    def test_presence_loggedin_but_no_email(self):
        """ when logged in but if the user has no email address then they should see the email input """
        user = User.objects.create_user('test-no-email', '', 'test') # user with no email
        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)
        self.assertIn('_auth_user_id', self.client.session)

        result = self.client.get(self.contact_us_url)

        soup = BeautifulSoup(result.content)
        emailElement = soup.findAll('input', id="id_email", type="text") # normal input

        self.assertTrue(len(emailElement) == 1)

    def test_presence_not_loggedin(self):
        """ when not logged in the user should see the email input """
        self.assertNotIn('_auth_user_id', self.client.session) # not logged in

        result = self.client.get(self.contact_us_url)

        soup = BeautifulSoup(result.content)

        nameElement = soup.findAll('input', id="id_name") # text
        emailElement = soup.findAll('input', id="id_email", type="text") # normal input

        self.assertTrue(len(emailElement) == 1)
        self.assertTrue('value' not in emailElement[0])

        self.assertTrue(len(nameElement) == 1)
        self.assertTrue('value' not in nameElement[0])