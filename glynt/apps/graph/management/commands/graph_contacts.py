# -*- coding: utf-8 -*-
""" 
Command to collect user connections from various services
"""
from django.core.management.base import BaseCommand
from optparse import make_option

from social_auth.models import UserSocialAuth

from glynt.apps.graph.services import LinkedinConnectionService, AngelConnectionService
from glynt.apps.graph.services import LinkedInProcessConnectionService, AngelProcessConnectionService


import json
from urlparse import parse_qs

import logging
logger = logging.getLogger('lawpal.graph')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--auth',
            dest='auth',
            default=None,
            help='A specific Authentication Object to use'),
        make_option('--provider_type',
            dest='provider_type',
            default=None,
            help='A specific Provider Type to check'),
    )

    help = 'Collects Contact Ids from various connected user Services'

    def handle(self, *args, **options):
        auth = options.get('auth', None)

        self.provider_type = options.get('provider_type', None)

        if auth is not None:
            self.process_single_auth(auth)
        else:
            self.process_all_auth()

    def process_single_auth(self, auth):
        if type(auth) is not UserSocialAuth:
            logger.error('Cloud not Process Auth Graph collection as its not a UserSocialAuth class it is a %s' % type(auth))
        else:
            if auth.provider == 'linkedin':
                self.linkedin(auth)
            elif auth.provider == 'angel':
                self.angel(auth)
            else:
                raise Exception('Unknown Auth Provider %s' % auth.provider)

    def get_queryset(self):
        qs = UserSocialAuth.objects.prefetch_related('user')
        if self.provider_type is not None:
            qs = qs.filter(provider=self.provider_type)
        else:
            qs = qs.all()
        return qs

    def process_all_auth(self):
        for auth in self.get_queryset():
            self.process_single_auth(auth)

    def linkedin(self, auth):
        if auth.provider == 'linkedin':
            user_access_data = parse_qs(auth.extra_data.get('access_token'))

            oauth_client = LinkedinConnectionService(oauth_token=user_access_data.get('oauth_token')[0], \
                                                    oauth_token_secret=user_access_data.get('oauth_token_secret')[0])
            resp, content = oauth_client.request()

            content = json.loads(content)
            contacts = content.get('values', [])
            logger.info('LinkedIn contacts:%d for %s '%(len(contacts), auth.user.username,))
            logger.debug('LinkedIn response:%s for %s '%(resp, auth.user.username,))

            for u in contacts:
                # linked in uses "id" and not uid
                LinkedInProcessConnectionService(item=u, uid=u.get('id'), user=auth.user)

    def angel(self, auth):
        if auth.provider == 'angel':
            access_token = auth.extra_data.get('access_token')

            # initial values
            complete = False
            current_page = 1

            logger.info('Starting angel contact graph import for %s' % auth)

            # Basic Pagination
            while not complete:
                oauth_client = AngelConnectionService(access_token=access_token, angel_uid=auth.uid, page=current_page)
                resp, content = oauth_client.request()

                # decode the json
                content = json.loads(content)

                # get the page info
                current_page = int(content.get('page', 1))
                last_page = int(content.get('last_page', 1))
                logger.info('page %d or %d for angel auth: %s' % (last_page, current_page, auth,))

                contacts = content.get('users', [])
                logger.info('AngelList in contacts:%d for %s '%(len(contacts), auth.user.username,))
                logger.debug('AngelList in response:%s for %s '%(resp, auth.user.username,))
                for u in contacts:
                    if u.get('id', None) is not None:
                        AngelProcessConnectionService(uid=u.get('id'), item=u, user=auth.user)

                complete = bool(current_page >= last_page)
