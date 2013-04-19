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

from guardian.shortcuts import assign

from django_countries import CountryField


import logging
logger = logging.getLogger('django.request')

LAWPAL_PRIVATE_BETA = getattr(settings, 'LAWPAL_PRIVATE_BETA', False)



class ClientProfile(UserenaBaseProfile):
    """ Base User Profile, where we store all the interesting information about users """
    user = models.OneToOneField(User, unique=True, related_name='profile')
    profile_data = JSONField(blank=True, null=True)
    country = CountryField(default='US', null=True)
    state = models.CharField(max_length=64, null=True)

    @classmethod
    def create(cls, **kwargs):
        profile = cls(**kwargs)
        profile.save()
        return profile

    def short_name(self):
        """ Returns A. LastName """
        user = self.user
        return u'%s. %s' % (user.first_name[0], user.last_name,) if user.first_name and user.last_name else user.username

# set the profile
User.profile = property(lambda u: ClientProfile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_client_profile', )
def create_client_profile(sender, **kwargs):
    """ Method creates the permissions required for the current user
    to view their account info and edit passwrds etc """
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if profile is not None and is_new == True:
        user = profile.user
        logger.info('Creating Profile Permissions for User %s' % user.username)
        # Give permissions to view and change profile
        for perm, name in ASSIGNED_PERMISSIONS['profile']:
            assign(perm, user, profile)

        # Give permissions to view and change itself
        for perm, name in ASSIGNED_PERMISSIONS['user']:
            assign(perm, user, user)

        # Send the signup complete signal
        userena_signals.signup_complete.send(sender=None, user=user)


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_lawyer_profile')
def create_lawyer_profile(sender, **kwargs):
    profile = kwargs.get('instance', None)
    user = profile.user

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
        userena_signup, is_new = UserenaSignup.objects.create_userena_profile(user=profile.user)

