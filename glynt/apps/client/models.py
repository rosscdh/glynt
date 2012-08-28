from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from jsonfield import JSONField

from socialregistration.signals import login, connect, profile_data
from userena.models import UserenaSignup, UserenaBaseProfile
from userena.managers import ASSIGNED_PERMISSIONS
from guardian.shortcuts import assign, get_perms

from django_countries import CountryField
from managers import GlyntUserManager as UserManager

import urllib2


class UserSignup(UserenaSignup):
  """ Override the manager as we do some funky things """
  objects = UserManager()


class ClientProfile(UserenaBaseProfile):
  """ Base User Profile, where we store all the interesting information about users """
  user = models.OneToOneField(User,
                              unique=True,
                              related_name='my_profile')
  profile_data = JSONField(blank=True, null=True)
  country = CountryField(default='US', null=True)
  state = models.CharField(max_length=64, null=True)

  def get_mugshot_url(self):
    """ Override the default """
    # @TODO on save to thumbnail image; write a task that
    # processes remote urls and downloads them locally
    url = super(ClientProfile, self).get_mugshot_url()
    validate = URLValidator(verify_exists=False)
    tmp_url = urllib2.unquote(url.replace(settings.MEDIA_URL,''))
    try:
      validate(tmp_url)
      # remove the static url from it
      url = tmp_url
    except ValidationError, e:
      pass

    return url


class ClientContactsList(models.Model):
  """ Model to store a list of the clients contacts in the form:
  {
  'name': '',
  'picture': '',
  'extra': {'id': <int>id, 'service': 'facebook', 'data_type': 'friends'}
  }
  """
  user = models.OneToOneField(User)
  data = JSONField(blank=True, null=True)


@receiver(connect)
def create_client_profile(sender, **kwargs):
  user = kwargs['user']
  profile, is_new = ClientProfile.objects.get_or_create(user=user)
  # @TODO turn this process into a signal so it can be called for other signup types
  if is_new:
    # Give permissions to view and change profile
    for perm in ASSIGNED_PERMISSIONS['profile']:
        assign(perm[0], user, profile)

    # Give permissions to view and change itself
    for perm in ASSIGNED_PERMISSIONS['user']:
        assign(perm[0], user, user)


@receiver(login)
@receiver(connect)
def populate_profile_data(sender, **kwargs):
  user = kwargs['user']
  profile, is_new = ClientProfile.objects.get_or_create(user=user)
  if 'profile_data' in kwargs:
    profile.profile_data = kwargs['profile_data']

    # Handle facebook profile_photo
    if 'profile_photo' in profile.profile_data:
      # @TODO on save to thumbnail image; write a task that
      # processes remote urls and downloads them locally
      validate = URLValidator(verify_exists=True)
      try:
        validate(profile.profile_data['profile_photo'])
        profile.mugshot = profile.profile_data['profile_photo']
      except ValidationError, e:
        pass

  profile.save()

