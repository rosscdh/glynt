# -*- coding: utf-8 -*-
"""
"""
from django.conf import settings

ABRIDGE_API_URL = getattr(settings, 'ABRIDGE_API_URL', 'http://localhost:8001/')

ABRIDGE_ACCESS_KEY_ID = getattr(settings, 'ABRIDGE_ACCESS_KEY_ID', None)
ABRIDGE_SECRET_ACCESS_KEY = getattr(settings, 'ABRIDGE_SECRET_ACCESS_KEY', None)
ABRIDGE_PROJECT = getattr(settings, 'ABRIDGE_PROJECT', None)

if ABRIDGE_ACCESS_KEY_ID is None:
    raise Exception("You must specify a ABRIDGE_ACCESS_KEY_ID in your settings.py")
if ABRIDGE_SECRET_ACCESS_KEY is None:
    raise Exception("You must specify a ABRIDGE_SECRET_ACCESS_KEY in your settings.py")
if ABRIDGE_PROJECT is None:
    raise Exception("You must specify a ABRIDGE_PROJECT in your settings.py")


class ConnectionBase(object):
    client = None
    consumer = oauth.Consumer(ABRIDGE_ACCESS_KEY_ID, ABRIDGE_SECRET_ACCESS_KEY)
    url = ABRIDGE_API_URL

    def __init__(self, consumer=None, url=None, **kwargs):
        self.consumer = consumer if consumer is not None else self.consumer
        self.url = url if url is not None else self.url
        # append kwargs to class
        self.__dict__.update(kwargs)

    def get_url(self):
        return self.url

    def get_client(self):
        return oauth.Client(consumer=self.consumer)

    def request(self, method='GET'):
        access_token = oauth.Token(
                    key=getattr(self, 'oauth_token'),
                    secret=getattr(self, 'oauth_token_secret'))
        self.client = client = oauth.Client(self.consumer, access_token)
        return super(LinkedinConnectionService, self).request(method=method, client=client)