"""
Test the default app and Facebook integration
"""
from django.conf import settings
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class FacebookLoginTest(TestCase):
    fixtures = ['test_users.json', 'sites.json', 'cms.json']

    def setUp(self):
        self.client = Client()

        self.user = mommy.make('auth.User', username='customer', first_name='Customer', last_name='A', email='customer+test@lawpal.com')
        self.user.set_password('test')
        self.user.save()

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
        FB_PERMS = settings.FACEBOOK_REQUEST_PERMISSIONS.split(',')
        for perm in ['email', 'user_likes', 'user_about_me', 'read_stream']:
            self.assertTrue(perm in FB_PERMS)
