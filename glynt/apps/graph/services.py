# -*- coding: utf-8 -*-
from django.conf import settings
from models import LawpalBaseConnection
import oauth2 as oauth


class ProcessConnectionsService(object):
    provider = 'unknown'

    def __init__(self, uid, item, **kwargs):
        self.connection_class = kwargs.get('connection_class', LawpalBaseConnection)
        self.uid = uid

        self.__dict__.update(item)

        self.process(item)

    def process(self, item):
        self.connection = self.connection_class(provider=self.provider, uid=self.uid, **item)



class LinkedInProcessConnectionsService(ProcessConnectionsService):
    provider = 'linkedin'


class AngelProcessConnectionsService(ProcessConnectionsService):
    provider = 'angel'


"""
The Collector Services
Used to Query the remote 3rd Party Api
"""

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
        return oauth.Client(consumer=self.consumer)

    def request(self, method='GET', **kwargs):
        client = self.get_client() if kwargs.get('client', None) is None else kwargs.get('client')
        return client.request(self.get_url(), method, '')


class LinkedinConnectionsService(CollectConnectionsBaseService):
    consumer = oauth.Consumer(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET)
    url = 'http://api.linkedin.com/v1/people/~/connections?format=json'

    def request(self, method='GET'):
        access_token = oauth.Token(
                    key=getattr(self, 'oauth_token'),
                    secret=getattr(self, 'oauth_token_secret'))
        client = oauth.Client(self.consumer, access_token)
        return super(LinkedinConnectionsService, self).request(method=method, client=client)


class AngelConnectionsService(CollectConnectionsBaseService):
    consumer = oauth.Consumer(settings.ANGEL_CLIENT_ID, settings.ANGEL_CLIENT_SECRET)
    url = 'https://api.angel.co/1/users/%s/followers?access_token=%s'

    def get_url(self):
        return self.url % (getattr(self, 'user_id'), getattr(self, 'access_token'))