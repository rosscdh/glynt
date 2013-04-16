# -*- coding: utf-8 -*-
""" 
Command to collect user connections from various services
"""
import sys
from django.conf import settings
from django.core.management.base import BaseCommand

from social_auth.models import UserSocialAuth

from glynt.apps.graph.services import LinkedInProcessConnectionsService, AngelProcessConnectionsService
from glynt.apps.graph.services import LinkedinConnectionsService, AngelConnectionsService

import json
from urlparse import parse_qs
import pdb


class Command(BaseCommand):
    help = 'Collects Contact Ids from various connected user Services'

    def handle(self, *args, **options):

        for a in UserSocialAuth.objects.prefetch_related('user').all():
            if a.provider == 'linkedin':
                self.linkedin(a)

            if a.provider == 'angel':
                self.angel(a)

    def linkedin(self, auth):
        if auth.provider == 'linkedin':
            user_access_data = parse_qs(auth.extra_data.get('access_token'))

            oauth_client = LinkedinConnectionsService(oauth_token=user_access_data.get('oauth_token')[0], \
                                                    oauth_token_secret=user_access_data.get('oauth_token_secret')[0])
            resp, content = oauth_client.request()

            content = json.loads(content)

            for u in content.get('values'):
                c = LinkedInProcessConnectionsService(item=u, uid=u.get('uid'), user=auth.user)
                print c.connection

    def angel(self, auth):
        if auth.provider == 'angel':
            access_token = auth.extra_data.get('access_token')

            oauth_client = AngelConnectionsService(access_token=access_token, angel_uid=auth.uid)
            resp, content = oauth_client.request()

            content = json.loads(content)

            for u in content.get('users', []):
                if u.get('id', None) is not None:
                    c = AngelProcessConnectionsService(uid=u.get('id'), item=u, user=auth.user)
                    print c.connection


    def twitter(self):
        pass