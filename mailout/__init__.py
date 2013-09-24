# -*- coding: utf-8 -*-
"""
"""
from django.conf import settings

import oauth2
import httplib2
import hashlib
import urllib
import json

ABRIDGE_API_URL = getattr(settings, 'ABRIDGE_API_URL', 'http://localhost:8001/')
ABRIDGE_PROJECT = getattr(settings, 'ABRIDGE_PROJECT', None)

ABRIDGE_ACCESS_KEY_ID = getattr(settings, 'ABRIDGE_ACCESS_KEY_ID', None)
ABRIDGE_SECRET_ACCESS_KEY = getattr(settings, 'ABRIDGE_SECRET_ACCESS_KEY', None)
ABRIDGE_USERNAME = getattr(settings, 'ABRIDGE_USERNAME', None)
ABRIDGE_PASSWORD = getattr(settings, 'ABRIDGE_PASSWORD', None)


if ABRIDGE_ACCESS_KEY_ID is None:
    raise Exception("You must specify a ABRIDGE_ACCESS_KEY_ID in your settings.py")
if ABRIDGE_SECRET_ACCESS_KEY is None:
    raise Exception("You must specify a ABRIDGE_SECRET_ACCESS_KEY in your settings.py")
if ABRIDGE_PROJECT is None:
    raise Exception("You must specify a ABRIDGE_PROJECT in your settings.py")
if ABRIDGE_USERNAME is None:
    raise Exception("You must specify a ABRIDGE_USERNAME in your settings.py")
if ABRIDGE_PASSWORD is None:
    raise Exception("You must specify a ABRIDGE_PASSWORD in your settings.py")

class UserGetOrCreateMixin(object):
    _access_token = None
    _user = None
    _email_hash = None
    _h = httplib2.Http(".cache")

    @property
    def access_token(self):
        if self._access_token is None:
            data = {
                'client_id': ABRIDGE_ACCESS_KEY_ID,
                'client_secret': ABRIDGE_SECRET_ACCESS_KEY,
                'grant_type': 'password',
                'username': ABRIDGE_USERNAME,
                'password': ABRIDGE_PASSWORD,
            }
            headers = {'Content-type': 'application/x-www-form-urlencoded'}

            resp, content = self._h.request(self.get_url(path='oauth2/access_token/'), "POST", headers=headers, body=urllib.urlencode(data))

            if resp.status in [200]:
                content = json.loads(content)
                self._access_token = content.get('access_token')
            else:
                raise Exception('Error in query: %s')

        return self._access_token

    def mailout_user(self):
        if self._user is None:
            self._email_hash = hashlib.md5(self.user.email).hexdigest()

            resp, content = self._h.request(self.get_url(path='user/{email_hash}/'.format(email_hash=self._email_hash)), "GET")
            
            if resp.status in [404]:
                self._user = self.create_user()

        return self._user

    def create_user(self):
        user_data = {
            'username': self.user.username,
            'email': self.user.email
        }

        resp, content = self.request(path='user/', data=user_data, method='POST')

        return json.loads(content)


class MailoutConnectionBase(UserGetOrCreateMixin):
    client = None
    consumer = oauth2.Consumer(ABRIDGE_ACCESS_KEY_ID, ABRIDGE_SECRET_ACCESS_KEY)
    base_uri = ABRIDGE_API_URL

    def __init__(self, consumer=None, url=None, **kwargs):
        self.consumer = consumer if consumer is not None else self.consumer
        self.base_uri = url if url is not None else self.base_uri
        # append kwargs to class
        self.__dict__.update(kwargs)

    def get_url(self, path):
        return '{base}{path}'.format(base=self.base_uri, path=path)

    def request(self, path, data=None, method='GET', **kwargs):
        headers = {
                    'Authorization': 'Bearer 63f04de9e2ad088d29c8d418adc0206f996d307b',
                    'Content-type': 'application/x-www-form-urlencoded',
                }
        data = urllib.urlencode(data) if data is not None else None
        resp, content = self._h.request(self.get_url(path=path), method, headers=headers, body=data)
        return json.loads(content)
