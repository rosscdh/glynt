# -*- coding: utf-8 -*-
"""
lawpal Graph Services
Used to both query the 3rd party apis
as well as process the response items and add
them to the graph database models
"""
from django.conf import settings

from models import LawpalBaseConnection, LinkedinConnection, AngelConnection, FullContactConnection
from models import GraphConnection

from BeautifulSoup import BeautifulSoup
import oauth2 as oauth
import requests
import json


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

        # update the local class dic with the item so we can refer to the values directly
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


class FullContactProcessConnectionService(ProcessConnectionService):
    provider = 'fullcontact'
    connection_class = FullContactConnection


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


class LinkedinProfileService(LinkedinConnectionService):
    url = 'http://api.linkedin.com/v1/people/%s'
    linkedin_user_profile = None
    def get_url(self):
        """ allow ability to specify the user to query 
        default is ~ or current logged in user """
        return self.url % '%s:(picture-url,current-status,industry,summary)'%self.uid if self.uid else '~'

    @property
    def profile(self):
        if self.linkedin_user_profile is None:
            resp, content = self.request()

            p = BeautifulSoup(content)

            # parse the crzy linked in api
            self.linkedin_user_profile = {
                'photo_url': p.person.find('picture-url').string if p.person.find('picture-url') is not None else None,
                'status': p.person.find('current-status').string if p.person.find('current-status') is not None else None,
                'industry': p.person.find('industry').string if p.person.find('industry') is not None else None,
                'summary': p.person.find('summary').string if p.person.find('summary') is not None else None,

            }
        return self.linkedin_user_profile


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


class FullContactConnectionService(CollectConnectionBaseService):
    consumer = requests # python reqeusts library
    url = 'https://api.fullcontact.com/v2/person.json?email={email}&apiKey={access_token}&page={page}'

    def get_url(self):
        page = getattr(self, 'page', 1)
        return self.url.format(email=getattr(self, 'email'), access_token=getattr(self, 'access_token'), page=page)

    def request(self, method='GET', **kwargs):
        """ we dont use oauth for FullContact just a direct requests """
        url = self.get_url()
        action_method = method.lower()

        # call the consumer (requests object) and pass it the generated url
        response = getattr(self.consumer, action_method)(url)

        # return as a tuple to be the same as oauth requests
        return (response, response.json(),)

