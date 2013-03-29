"""
Test the default app and Facebook integration
"""
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from glynt.apps.factories import UserFactory
#from socialregistration.contrib.facebook_js.context_processors import FACEBOOK_REQUEST_PERMISSIONS



class FacebookLoginTest(TestCase):
    fixtures = ['test_users.json', 'sites.json', 'cms.json']

    def setUp(self):
        user = UserFactory.create(pk=1)
        self.client = Client()

        password = make_password('test')
        self.usera, is_new = User.objects.get_or_create(username='testa', password=password, email='testa@weareml.com')


    def test_presence_of_facebook_button_on_login_and_signup(self):
        """ Facebook button should only be on the login and signup pages"""
        urls = [reverse('client:login'), reverse('client:signup')]
        for url in urls:
            response = self.client.get(url, follow=True)
            fb_button_login = 'id="connect-facebook"'
            self.assertContains(response, fb_button_login, status_code=200)
            self.assertContains(response, 'FB.init({', status_code=200)
            self.assertContains(response, 'var csrftoken =', status_code=200)
            self.assertContains(response, 'https://graph.facebook.com/oauth/access_token?client_id=', status_code=200)

    def test_facebook_request_permissions(self):
        FB_PERMS = FACEBOOK_REQUEST_PERMISSIONS.split(',')
        for perm in ['email', 'user_likes', 'user_about_me', 'read_stream']:
            self.assertTrue(perm in FB_PERMS)
