from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save

from jsonfield import JSONField

from userena.models import UserenaSignup, UserenaBaseProfile
from userena.managers import ASSIGNED_PERMISSIONS
from userena import signals as userena_signals

from glynt.apps.lawyer.services import EnsureLawyerService
from glynt.apps.startup.services import EnsureFounderService, EnsureStartupService

from templated_email import send_templated_mail

from guardian.shortcuts import assign_perm

from django_countries import CountryField


import logging
logger = logging.getLogger('django.request')

LAWPAL_PRIVATE_BETA = getattr(settings, 'LAWPAL_PRIVATE_BETA', False)



class ClientProfile(UserenaBaseProfile):
    """ Base User Profile, where we store all the interesting information about users """
    user = models.OneToOneField(User, unique=True, related_name='profile')
    profile_data = JSONField(default={})
    country = CountryField(default='US', null=True)
    state = models.CharField(max_length=64, null=True)
    is_lawyer = models.BooleanField(default=True)

    @classmethod
    def create(cls, **kwargs):
        profile = cls(**kwargs)
        profile.save()
        return profile

    def get_mugshot_url(self):
        p = self.profile_data.get('linkedin_photo_url', None) or self.profile_data.get('facebook_photo_url', None) or super(ClientProfile, self).get_mugshot_url()
        return p

    @property
    def user_class(self):
        return self.profile_data.get('user_class_name', None)

    @property
    def is_lawyer(self):
        return True if self.user_class == 'lawyer' else False

    @property
    def is_startup(self):
        return True if self.user_class == 'startup' else False

    def short_name(self):
        """ Returns A. LastName """
        user = self.user
        return u'%s. %s' % (user.first_name[0], user.last_name,) if user.first_name and user.last_name else user.username


def _create_user_profile(user):
    # set the profile
    # This is what triggers the whole cleint profile creation process in pipeline.py:ensure_user_setup
    return ClientProfile.objects.get_or_create(user=user)

# used to trigger profile creation by accidental refernce. Rather use the _create_user_profile def above
User.profile = property(lambda u: _create_user_profile(user=u)[0])


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_client_profile', )
def create_client_profile(sender, **kwargs):
    """ Method creates the permissions required for the current user
    to view their account info and edit passwrds etc """
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', False)

    if profile is not None and is_new == True:
        user = profile.user
        logger.info('Creating Profile Permissions for User %s' % user.username)
        # Give permissions to view and change profile
        for perm, name in ASSIGNED_PERMISSIONS['profile']:
            assign_perm(perm, user, profile)

        # Give permissions to view and change itself
        for perm, name in ASSIGNED_PERMISSIONS['user']:
            assign_perm(perm, user, user)

        # Send the signup complete signal
        userena_signals.signup_complete.send(sender=None, user=user)


def create_glynt_profile(profile, is_new):
    """ function used to create the appropriate glynt profile type
    for a user signing in """
    user = profile.user
    user_class_name = profile.user_class

    if profile is not None and is_new == True:
        if profile.is_startup:
            logger.info('Creating Founder Profile for User %s' % user.username)
            founder_service = EnsureFounderService(user=user)
            founder_service.process()

        elif profile.is_lawyer:
            logger.info('Creating Lawyer Profile for User %s' % user.username)
            lawyer_service = EnsureLawyerService(user=user)
            lawyer_service.process()

        else:
            raise Exception('Could not identify user class by session')


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_userarena_signup')
def create_userarena_signup(sender, **kwargs):
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if profile is not None and is_new == True:
        user = profile.user
        logger.info('Creating UserenaSignup object for User %s' % user.username)
        userena_signup = UserenaSignup.objects.create_userena_profile(user=user)

