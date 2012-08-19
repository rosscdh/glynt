"""
Test the default app and Facebook integration
"""
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from socialregistration.contrib.facebook_js.context_processors import FACEBOOK_REQUEST_PERMISSIONS

class FacebookLoginTest(TestCase):
  def setUp(self):
    self.client = Client()

    password = make_password('test')
    self.usera, is_new = User.objects.get_or_create(username='testa', password=password, email='testa@weareml.com')

  def test_lack_of_presence_of_facebook_button_on_root(self):
    response = self.client.get(reverse('glynt:default'), follow=True)
    fb_button_login = '<fb:login-button id="fb_login-button"'
    self.assertNotContains( response, fb_button_login, status_code=200 )

  def test_presence_of_facebook_button_on_login_and_signup(self):
    """ Facebook button should only be on the login and signup pages"""
    urls = [reverse('client:login'), reverse('client:signup')]
    for url in urls:
      response = self.client.get(url, follow=True)
      fb_button_login = '<fb:login-button id="fb_login-button" size="large" scope="%s" on-login="SocialFBLogin();">Connect with Facebook</fb:login-button>' \
      % (FACEBOOK_REQUEST_PERMISSIONS,)
      self.assertContains( response, fb_button_login, status_code=200 )

  def test_facebook_request_permissions(self):
    FB_PERMS = FACEBOOK_REQUEST_PERMISSIONS.split(',')
    for perm in ['email', 'user_likes', 'user_about_me', 'read_stream']:
        self.assertTrue(perm in FB_PERMS)

