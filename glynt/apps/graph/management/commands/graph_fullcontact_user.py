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
from glynt.apps.graph.models import FullContactData

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

        self.pk = options.get('pk', None)
        if self.pk is not None and type(self.pk) != int:
            raise Exception('--pk must be an integer')

        if self.pk is not None and type(self.pk) is int:
            logger.info('FullContact import PK has been specified: %s' % self.pk)
            self.process_single_user(self.get_queryset(filter_options={'pk':self.pk})[0])
        else:
            self.process_all_user()

    def process_single_user(self, user):
        self.fullcontact(user)

    def get_queryset(self, filter_options=None):
        qs = User.objects.exclude(email='')
        if filter_options is not None:
            qs = qs.filter(**filter_options)
        else:
            qs = qs.all()
        return qs

    def process_all_user(self):
        for user in self.get_queryset():
            self.process_single_user(user)

    def fullcontact(self, user):
        """ Process the fullcontact data for a users email """
        logger.info('Starting FullContact info import for %s' % user.pk)
        # Get the user FC data object
        fc_data, is_new = FullContactData.objects.get_or_create(user=user)
        if is_new is True or fc_data.extra_data.get('contactInfo',None) is None:
            logger.info('FullContact User needs data from FullContact: %s (%s) is_new: %s' % (user.username, user.pk, is_new,))
            client = FullContactConnectionService(access_token=self.access_token, email=user.email)
            resp, json_content = client.request()

            contact_info = json_content.get('contactInfo', None)

            # if we have found a FC user object
            if contact_info is not None:
                logger.info('FullContact User Found: %s (%s) is_new: %s' % (user.username, user.pk, is_new,))
                fc_data.extra_data = json_content
                fc_data.save(update_fields=['extra_data'])
