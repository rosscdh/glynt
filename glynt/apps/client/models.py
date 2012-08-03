from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.dispatch import receiver
from socialregistration.signals import connect, profile_data

from jsonfield import JSONField

from userena.models import UserenaSignup, UserenaBaseProfile
from django_countries import CountryField
from managers import GlyntUserManager as UserManager


class UserSignup(UserenaSignup):
  """ Override the manager as we do some funky things """
  objects = UserManager()


class ClientProfile(UserenaBaseProfile):
  """ Base User Profile, where we store all the interesting information about users """
  user = models.OneToOneField(User,
                              unique=True,
                              verbose_name=_('user'),
                              related_name='my_profile')
  profile_data = JSONField(blank=True, null=True)
  country = CountryField(default='US')
  state = models.CharField(max_length=64, null=True)
  # company = models.CharField(_('Company'), max_length=5)
  # position = models.CharField(_('Position'), max_length=5)


@receiver(connect)
def create_client_profile(sender, **kwargs):
  user = kwargs['user']
  profile, is_new = ClientProfile.objects.get_or_create(user=user)


@receiver(connect)
def populate_profile_data(sender, **kwargs):
  user = kwargs['user']
  profile_data = kwargs['profile_data']
  profile, is_new = ClientProfile.objects.get_or_create(user=user)
  profile.profile_data = profile_data
  profile.save()

