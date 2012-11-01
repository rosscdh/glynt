from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, UserManager, Permission, AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.conf import settings

from userena import settings as userena_settings
from userena.utils import generate_sha1, get_profile_model, get_datetime_now
from userena import signals as userena_signals

from userena.managers import UserenaManager, SHA1_RE, ASSIGNED_PERMISSIONS
from guardian.shortcuts import assign, get_perms


class GlyntUserManager(UserenaManager):

  def create_user(self, username, email, password, active=False, send_email=True, *args, **kwargs):
    """
    A simple wrapper that creates a new :class:`User`.

    :param username:
        String containing the username of the new user.

    :param email:
        String containing the email address of the new user.

    :param password:
        String containing the password for the new user.

    :param active:
        Boolean that defines if the user requires activation by clicking 
        on a link in an e-mail. Defaults to ``False``.

    :param send_email:
        Boolean that defines if the user should be send an email. You could
        set this to ``False`` when you want to create a user in your own
        code, but don't want the user to activate through email.

    :**kwargs *:
        Pass named arguments into the method to save those fields to the 
        corresponding model

    :return: :class:`User` instance representing the new user.

    """
    now = get_datetime_now()

    new_user = User.objects.create_user(username, email, password)
    new_user.is_active = active
    new_user.save()

    userena_profile = self.create_userena_profile(new_user)

    # All users have an empty profile
    profile_model = get_profile_model()

    try:
        new_profile = new_user.get_profile()
    except profile_model.DoesNotExist:
        new_profile = profile_model(user=new_user)

    # Set the values of the model should they be passed in
    # This is the primary custommisation to this method
    # The User object
    for key,value in kwargs.iteritems():
      if hasattr(new_user, key):
        setattr(new_user, key, value)
    new_user.save(using=self._db)

    # The user.profile object
    for key,value in kwargs.iteritems():
      if hasattr(new_profile, key):
        setattr(new_profile, key, value)
    new_profile.save(using=self._db)

    # Give permissions to view and change profile
    for perm in ASSIGNED_PERMISSIONS['profile']:
        assign(perm[0], new_user, new_profile)

    # Give permissions to view and change itself
    for perm in ASSIGNED_PERMISSIONS['user']:
        assign(perm[0], new_user, new_user)

    if send_email:
        userena_profile.send_activation_email()

    return new_user
