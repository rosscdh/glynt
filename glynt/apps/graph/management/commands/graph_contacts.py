# -*- coding: utf-8 -*-
""" 
Command to collect user connections from various services
"""
import sys
from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option

from social_auth.models import UserSocialAuth

from glynt.apps.graph.services import LinkedInProcessConnectionService, AngelProcessConnectionService
from glynt.apps.graph.services import LinkedinConnectionService, AngelConnectionService

import json
from urlparse import parse_qs
import pdb


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--auth',
            action='store_true',
            dest='auth',
            default=None,
            help='A specific Authentication Object to use'),
    )

    help = 'Collects Contact Ids from various connected user Services'

    def handle(self, *args, **options):
        auth = options.get('auth', None)
        if auth is not None:
            self.process_single_auth(auth)
        else:
            self.process_all_auth()

    def process_single_auth(self, auth):
        if auth.provider == 'linkedin':
            self.linkedin(auth)
        elif auth.provider == 'angel':
            self.angel(auth)
        else:
            raise Exception('Unknown Auth Provider %s' % auth.provider)

    def process_all_auth(self):
        for auth in UserSocialAuth.objects.prefetch_related('user').all():
            self.process_single_auth(auth)

    def linkedin(self, auth):
        if auth.provider == 'linkedin':
            user_access_data = parse_qs(auth.extra_data.get('access_token'))

            oauth_client = LinkedinConnectionService(oauth_token=user_access_data.get('oauth_token')[0], \
                                                    oauth_token_secret=user_access_data.get('oauth_token_secret')[0])
            resp, content = oauth_client.request()

            content = json.loads(content)

            for u in content.get('values'):
                c = LinkedInProcessConnectionService(item=u, uid=u.get('uid'), user=auth.user)

    def angel(self, auth):
        if auth.provider == 'angel':
            access_token = auth.extra_data.get('access_token')

            oauth_client = AngelConnectionService(access_token=access_token, angel_uid=auth.uid)
            resp, content = oauth_client.request()

            content = json.loads(content)

            for u in content.get('users', []):
                if u.get('id', None) is not None:
                    c = AngelProcessConnectionService(uid=u.get('id'), item=u, user=auth.user)

    def twitter(self):
        pass