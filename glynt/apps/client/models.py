# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.db.models.signals import post_save

from jsonfield import JSONField

from userena.models import UserenaSignup, UserenaBaseProfile
from userena.managers import ASSIGNED_PERMISSIONS
from userena import signals as userena_signals

from glynt.apps.lawyer.services import EnsureLawyerService
from glynt.apps.customer.services import EnsureCustomerService

from guardian.shortcuts import assign_perm

from django_countries import CountryField


import logging
logger = logging.getLogger('django.request')


class ClientProfile(UserenaBaseProfile):
    """ Base User Profile, where we store all the interesting information about users """
    user = models.OneToOneField(User, unique=True, related_name='profile')
    profile_data = JSONField(default={})
    country = CountryField(default='US', null=True)
    state = models.CharField(max_length=64, blank=True, null=True)

    @classmethod
    def create(cls, **kwargs):
        profile = cls(**kwargs)
        profile.save()
        return profile

    def get_mugshot_url(self):
        pic = None

        if self.is_lawyer:
            pic = self.user.lawyer_profile.profile_photo
        if self.is_customer:
            pic = self.user.customer_profile.profile_photo

        if pic is not None:
            return pic
        else:
            return super(ClientProfile, self).get_mugshot_url()

    @property
    def phone(self):
        return self.profile_data.get('phone', None)

    @property
    def user_class(self):
        return self.profile_data.get('user_class_name', None)

    @property
    def is_lawyer(self):
        return True if self.user_class == 'lawyer' else False

    @property
    def is_customer(self):
        return True if self.user_class == 'customer' else False

    @property
    def non_specific_title(self):
        if self.is_lawyer:
            return 'The Lawyer'
        if self.is_customer:
            return 'The Customer'
        return None

    def short_name(self):
        """ Returns A. LastName """
        user = self.user
        return u'%s. %s' % (user.first_name[0], user.last_name,) if user.first_name and user.last_name else user.username


def _get_or_create_user_profile(user):
    # set the profile
    # This is what triggers the whole cleint profile creation process in pipeline.py:ensure_user_setup
    profile, is_new = ClientProfile.objects.get_or_create(user=user)  # added like this so django noobs can see the result of get_or_create
    return (profile, is_new,)

# used to trigger profile creation by accidental refernce. Rather use the _create_user_profile def above
User.profile = property(lambda u: _get_or_create_user_profile(user=u)[0])


def _assign_perms(user, profile):
    for perm, name in ASSIGNED_PERMISSIONS.get('profile', ()):
        assign_perm(perm, user, profile)

    # Give permissions to view and change itself
    for perm, name in ASSIGNED_PERMISSIONS.get('user', ()):
        assign_perm(perm, user, user)

@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_client_profile', )
def create_client_profile(sender, **kwargs):
    """ Method creates the permissions required for the current user
    to view their account info and edit passwrds etc """
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', False)

    if profile is not None and is_new is True:
        user = profile.user
        logger.info('Creating Profile Permissions for User %s' % user.username)
        # Give permissions to view and change profile
        try:
            _assign_perms(user, profile)
        except ObjectDoesNotExist:
            call_command('check_permissions')
            _assign_perms(user, profile)

        # Send the signup complete signal
        userena_signals.signup_complete.send(sender=None, user=user)


def create_glynt_profile(profile, is_new):
    """ function used to create the appropriate glynt profile type
    for a user signing in """
    logger.info('create_glynt_profile for User %s' % profile.user.pk)
    user = profile.user

    logger.info('User is of class %s' % profile.user_class)

    if not is_new:
        logger.info('create_glynt_profile profile is not new User %s' % profile.user.pk)
    else:
        if profile.is_customer:
            logger.info('Creating Customer Profile for User %s' % user.username)
            customer_service = EnsureCustomerService(user=user)
            customer_service.process()

        elif profile.is_lawyer:
            logger.info('Creating Lawyer Profile for User %s' % user.username)
            lawyer_service = EnsureLawyerService(user=user)
            lawyer_service.process()

        else:
            raise Exception('Could not identify user class')


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_userarena_signup')
def create_userarena_signup(sender, **kwargs):
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if profile is not None and is_new is True:
        user = profile.user
        logger.info('Creating UserenaSignup object for User %s' % user.username)
        UserenaSignup.objects.create_userena_profile(user=user)
