# -*- coding: utf-8 -*-
"""
lawpal Graph Services
Used to both query the 3rd party apis
as well as process the response items and add
them to the graph database models
"""
from django.conf import settings

from models import LawpalBaseConnection, LinkedinConnection, AngelConnection
from models import GraphConnection

import oauth2 as oauth

import logging
logger = logging.getLogger('lawpal.services')


class ProcessConnectionService(object):
    """ Class to provide accessor to the connection_class
    which can be one of LawpalBaseConnection or descendant objects """
    provider = 'unknown'
    connection_class = LawpalBaseConnection
    connection = None

    def __init__(self, uid, item, **kwargs):
        self.connection_class = kwargs.get('connection_class') if kwargs.get('connection_class', None) is not None else self.connection_class
        self.uid = uid
        self.connection = self.connection_class(provider=self.provider, uid=self.uid, **item)
        self.user = kwargs.get('user', None)

        logger.info('Connection process %s.%s' % (self.provider, self.uid))

        self.__dict__.update(item)

        self.process(item)

    def process(self, item):
        if self.user is None:
            logger.info('Connection %s.%s has no associated user' % (self.provider, self.uid))
        else:
            logger.info('Processing connection %s.%s for user %s' % (self.provider, self.uid, self.user.get_full_name()))
            self.connection.associate(user=self.user)


class LinkedInProcessConnectionService(ProcessConnectionService):
    provider = 'linkedin'
    connection_class = LinkedinConnection


class AngelProcessConnectionService(ProcessConnectionService):
    provider = 'angel'
    connection_class = AngelConnection


"""
The Collector Services
Used to Query the remote 3rd Party Api
"""

class CollectConnectionBaseService(object):
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


class LinkedinConnectionService(CollectConnectionBaseService):
    consumer = oauth.Consumer(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET)
    url = 'http://api.linkedin.com/v1/people/~/connections?format=json'

    def request(self, method='GET'):
        access_token = oauth.Token(
                    key=getattr(self, 'oauth_token'),
                    secret=getattr(self, 'oauth_token_secret'))
        client = oauth.Client(self.consumer, access_token)
        return super(LinkedinConnectionService, self).request(method=method, client=client)


class AngelConnectionService(CollectConnectionBaseService):
    consumer = oauth.Consumer(settings.ANGEL_CLIENT_ID, settings.ANGEL_CLIENT_SECRET)
    url = 'https://api.angel.co/1/users/%s/followers?access_token=%s&page=%d'

    def get_client(self):
        """ Disable the ssl validation for angel they have ssl problems"""
        client = oauth.Client(consumer=self.consumer)
        client.disable_ssl_certificate_validation = True
        return client

    def get_url(self):
        page = getattr(self, 'page', 1)
        return self.url % (getattr(self, 'angel_uid'), getattr(self, 'access_token'), page)