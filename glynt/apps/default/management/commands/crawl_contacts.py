# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.core.management.base import BaseCommand

from social_auth.models import UserSocialAuth

import oauth2 as oauth
from urlparse import parse_qs

import pdb

class Command(BaseCommand):
    help = 'Collects Contact Ids from various connected user Services'

    def setup(self):
        self.linkedin_consumer = oauth.Consumer(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET)

    def handle(self, *args, **options):
        self.setup()

        for a in UserSocialAuth.objects.all():
            self.linkedin(a)

    def linkedin(self, auth):
        user_access_data = parse_qs(auth.extra_data.get('access_token'))

        access_token = oauth.Token(
                    key=user_access_data.get('oauth_token')[0],
                    secret=user_access_data.get('oauth_token_secret')[0])

        client = oauth.Client(self.linkedin_consumer, access_token)
        resp, content = client.request("http://api.linkedin.com/v1/people/~/connections?format=json", "GET", "")

    def angel(self):
        user_access_data = parse_qs(auth.extra_data.get('access_token'))
        pdb.set_trace()
        access_token = oauth.Token(
                    key=user_access_data.get('oauth_token')[0],
                    secret=user_access_data.get('oauth_token_secret')[0])

        client = oauth.Client(self.linkedin_consumer, access_token)
        resp, content = client.request("/users/%s/followers" % auth.extra_data.get('id') , "GET", "")

    def twitter(self):
        pass