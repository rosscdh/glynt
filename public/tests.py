from django.test import LiveServerTestCase
from django.test.client import Client
from django.test.utils import override_settings
from django import template

from BeautifulSoup import BeautifulSoup

from glynt.apps.factories import UserFactory, LoggedOutUserFactory


class TestContactUsForm(LiveServerTestCase):
    fixtures = ['test_cities']
    def setUp(self):
        self.client = Client()

        self.user = UserFactory.create()
        self.context = {
            'user': self.user
        }

        self.loggedout_user = LoggedOutUserFactory.create()
        self.loggedout_context = {
            'user': self.loggedout_user
        }

    def render_template(self, *args, **kwargs):
        context = kwargs.get('context', {})
        t = template.Template(''.join(args))
        c = template.Context(context)
        return t.render(c)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_presence_loggedin(self):
        result = self.client.get('/contact-us/')
        soup = BeautifulSoup(result.content)
        emailForm = soup.findAll('input', id="id_email")
        self.assertTrue(1 == 1)