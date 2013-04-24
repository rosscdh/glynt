# -*- coding: utf-8 -*-
""" 
Command to collect user connections from various services
"""
import sys
from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option

from django.contrib.auth.models import User

from glynt.apps.graph.services import FullContactConnectionService

import json
from urlparse import parse_qs

import logging
logger = logging.getLogger('lawpal.graph')


FULLCONTACT_API_KEY = getattr(settings, 'FULLCONTACT_API_KEY', None)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--pk',
            dest='pk',
            default=None,
            help='A specific user to populate'),
    )

    help = 'Collects the Fullcontact.com information about a user'

    def handle(self, *args, **options):
        if FULLCONTACT_API_KEY is None:
            raise Exception('You must define a FULLCONTACT_API_KEY in settings.py in order to use this service')

        self.access_token = FULLCONTACT_API_KEY

        self.pk = int(options.get('pk', 0))
        if self.pk == 0:
            raise Exception('--pk must be an integer')

        if self.pk is not None and type(self.pk) is int:
            logger.info('FullContact import PK has been specified: %s' % self.pk)
            self.process_single_user(self.get_queryset(filter_options={'pk':self.pk})[0])
        else:
            self.process_all_user()

    def process_single_user(self, user):
        self.fullcontact(user)


    def get_queryset(self, filter_options=None):
        qs = User.objects
        if filter_options is not None:
            qs = qs.filter(**filter_options)
        else:
            qs = qs.all()
        return qs

    def process_all_user(self):
        for user in self.get_queryset():
            self.process_single_user(user)

    def fullcontact(self, user):

        # initial values
        complete = False
        current_page = 1

        logger.info('Starting FullContact info import for %s' % self.pk)

        # Basic Pagination
        while not complete:
            client = FullContactConnectionService(access_token=self.access_token, email=user.email, page=current_page)
            resp, json_content = client.request()

            # get the page info
            current_page = int(json_content.get('page', 1))
            last_page = int(json_content.get('last_page', 1))
            logger.info('page %d or %d for FullContact: %s' % (last_page, current_page, user,))
            import pdb
            pdb.set_trace()

            complete = bool(current_page >= last_page)

