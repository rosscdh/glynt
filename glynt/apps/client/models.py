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

        # Give permissions to view and change profile
        for perm, name in ASSIGNED_PERMISSIONS['profile']:
            assign(perm, user, profile)

        # Give permissions to view and change itself
        for perm, name in ASSIGNED_PERMISSIONS['user']:
            assign(perm, user, user)

        # Send the signup complete signal
        userena_signals.signup_complete.send(sender=None, user=user)


@receiver(post_save, sender=ClientProfile, dispatch_uid='client.create_userarena_signup')
def create_userarena_signup(sender, **kwargs):
    profile = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if profile is not None and is_new == True:
        userena_signup, is_new = UserenaSignup.objects.get_or_create(user=profile.user)


# @receiver(post_save, sender=ClientProfile, dispatch_uid='client.private_beta_profile')
# def private_beta_profile(sender, **kwargs):
#     """ if the settings.LAWPAL_PRIVATE_BETA is True
#     then this method will diable the user account 
#     until we manually activate itself """
#     logger.info('LAWPAL_PRIVATE_BETA: %s' % LAWPAL_PRIVATE_BETA)

#     instance = kwargs.get('instance')
#     user = instance.user

#     if LAWPAL_PRIVATE_BETA is True:
#         logger.info('Deactivating User Account %d for manual activation' % user.pk)
#         user.is_active = False # Set to false to allow manual activation
#         user.save(update_fields=[is_active])

#     logger.debug('Sending private_beta_profile email')
#     send_templated_mail(
#         template_name = 'private_beta_new_user',
#         template_prefix="sign/email/",
#         from_email = 'website@lawpal.com',
#         recipient_list = [e for n,e in settings.MANAGERS],
#         context = kwargs
#     )