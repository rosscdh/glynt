# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.core.management.base import BaseCommand

from social_auth.models import UserSocialAuth

import oauth2 as oauth
import json
from urlparse import parse_qs

import pdb

class LawpalBaseConnection(object):
    id = None
    provider = None
    full_name = None
    extra_data = None

    def __init__(self, provider, uid, **kwargs):
        self.uid = uid
        self.provider = provider
        self.extra_data = kwargs
        self.full_name = self.get_full_name_from_data()

    def get_full_name_from_data(self):
        raise Exception('Not Implemented')

    def __str__(self):
        return '%s' % self.__unicode__().encode(sys.stdout.encoding)

    def __unicode__(self):
        return self.full_name


class LinkedinConnection(LawpalBaseConnection):
    def get_full_name_from_data(self):
        return u'%s %s' % (self.extra_data.get('firstName'), self.extra_data.get('lastName'),)


class AngelConnection(LawpalBaseConnection):
    def get_full_name_from_data(self):
        return u'%s' % self.extra_data.get('name')


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


class Command(BaseCommand):
    help = 'Collects Contact Ids from various connected user Services'

    def handle(self, *args, **options):

        for a in UserSocialAuth.objects.all():
            if a.provider == 'linkedin':
                self.linkedin(a)

            if a.provider == 'angel':
                self.angel(a)

    def linkedin(self, auth):
        if auth.provider == 'linkedin':
            user_access_data = parse_qs(auth.extra_data.get('access_token'))

            oauth_client = LinkedinConnectionsService(oauth_token=user_access_data.get('oauth_token')[0], oauth_token_secret=user_access_data.get('oauth_token_secret')[0])
            resp, content = oauth_client.request()
            content = json.loads(content)
            for u in content.get('values'):
                c = LinkedInProcessConnectionsService(item=u, uid=u.get('uid'), connection_class=LinkedinConnection)
                print c.connection

    def angel(self, auth):
        if auth.provider == 'angel':
            access_token = auth.extra_data.get('access_token')
            oauth_client = AngelConnectionsService(access_token=access_token, user_id=auth.uid)
            resp, content = oauth_client.request()

            content = json.loads(content)

            for u in content.get('users', []):
                if u.get('id', None) is not None:
                    c = AngelProcessConnectionsService(uid=u.get('id'), item=u, connection_class=AngelConnection)
                    print c.connection


    def twitter(self):
        pass