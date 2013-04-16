# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.core.management.base import BaseCommand

from social_auth.models import UserSocialAuth

import oauth2 as oauth
from urlparse import parse_qs

import pdb

class CollectConnectionsBaseService(object):
    consumer = None
    client = None
    url = None
    def __init__(self, consumer=None, url=None, **kwargs):
        self.consumer = consumer if consumer is not None else self.consumer
        self.url = url if url is not None else self.url
        # append kwargs to class
        self.__dict__.update(kwargs)

    def get_url(self):
        return self.url

    def get_client(self):
        return oauth.Client(consumer=self.consumer, token=getattr(self, 'access_token', None))

    def request(self, method='GET'):
        client = self.get_client()
        return client.request(self.get_url(), method, '')


class LinkedinConnectionsService(CollectConnectionsBaseService):
    consumer = oauth.Consumer(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET)
    url = 'http://api.linkedin.com/v1/people/~/connections?format=json'

    def request(self, method='GET'):
        access_token = oauth.Token(
                    key=getattr(self, 'oauth_token'),
                    secret=getattr(self, 'oauth_token_secret'))

        return super(LinkedinConnectionsService, self).request(method=method)

class AngelConnectionsService(CollectConnectionsBaseService):
    consumer = oauth.Consumer(settings.ANGEL_CLIENT_ID, settings.ANGEL_CLIENT_SECRET)
    url = 'https://api.angel.co/1/users/%s/followers?access_token=%s'

    def get_url(self):
        return self.url % (getattr(self, 'user_id'), getattr(self, 'access_token'))


class Command(BaseCommand):
    help = 'Collects Contact Ids from various connected user Services'

    def setup(self):
        self.linkedin_consumer = oauth.Consumer(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET)
        self.angel_consumer = oauth.Consumer(settings.ANGEL_CLIENT_ID, settings.ANGEL_CLIENT_SECRET)

    def handle(self, *args, **options):
        self.setup()

        for a in UserSocialAuth.objects.all():
            self.linkedin(a)
            self.angel(a)

    def linkedin(self, auth):
        if auth.provider == 'linkedin':
            user_access_data = parse_qs(auth.extra_data.get('access_token'))

            access_token = oauth.Token(
                        key=user_access_data.get('oauth_token')[0],
                        secret=user_access_data.get('oauth_token_secret')[0])

            client = oauth.Client(self.linkedin_consumer, access_token)
            resp, content = client.request("http://api.linkedin.com/v1/people/~/connections?format=json", "GET", "")

    def angel(self, auth):
        if auth.provider == 'angel':
            access_token = auth.extra_data.get('access_token')
            oauth_client = AngelConnectionsService(access_token=access_token, user_id=auth.uid)
            resp, content = oauth_client.request()

    def twitter(self):
        pass