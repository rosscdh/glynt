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

    def short_name(self):
        """ Returns A. LastName """
        user = self.user
        return u'%s. %s' % (user.first_name[0], user.last_name,) if user.first_name and user.last_name else user.username

# set the profile
# This is what triggers the whole cleint profile creation process in pipeline.py:ensure_user_setup
User.profile = property(lambda u: ClientProfile.objects.get_or_create(user=u)[0])


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


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_lawyer_profile')
def create_lawyer_profile(sender, **kwargs):
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', False)
    user = profile.user

    if profile is not None and is_new == True:
        logger.info('Creating Lawyer Profile for User %s' % user.username)
        lawyer_service = EnsureLawyerService(user=profile.user)
        lawyer_service.process()


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_userarena_signup')
def create_userarena_signup(sender, **kwargs):
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if profile is not None and is_new == True:
        user = profile.user
        logger.info('Creating UserenaSignup object for User %s' % user.username)
        userena_signup = UserenaSignup.objects.create_userena_profile(user=user)

