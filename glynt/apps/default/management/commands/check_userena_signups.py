# -*- coding: utf-8 -*-
""" 
Command to collect user connections from various services
"""
import sys
from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option

from django.contrib.auth.models import User
from userena.models import UserenaSignup

import datetime
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--user',
            dest='user',
            default=None,
            help='A specific Username or pk to check'),
        make_option('--send_email',
            dest='send_email',
            default=False,
            help='Send the invite Email'),
    )

    help = 'Collects Contact Ids from various connected user Services'

    def handle(self, *args, **options):
        self.user = options.get('user', None)
        send_email = options.get('send_email', False)

        for user in self.get_queryset():
            try:
                userena_signup = user.userena_signup
            except UserenaSignup.DoesNotExist:
                user.date_joined = datetime.datetime.utcnow()
                user.save(update_fields=['date_joined'])

                userena_signup = UserenaSignup.objects.create_userena_profile(user=user)

            if send_email:
                userena_signup.send_activation_email()

    def get_queryset(self):
        qs = User.objects

        if self.user is None:
            qs = qs.all()
        elif self.user.isdigit():
            qs = qs.filter(pk=int(self.user))
        elif self.user.isalnum():
            qs = qs.filter(username=self.user)
        else:
            raise Exception('%s is not a valid --user options: enter an pk or a username')
        return qs