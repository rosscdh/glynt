# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from social_auth.models import UserSocialAuth

from glynt.apps.client.models import _get_or_create_user_profile, create_glynt_profile
from glynt.apps.services.linkedin.pipeline import linkedin_profile_extra_details
from glynt.apps.services.google.pipeline import google_profile_extra_details

import uuid
import logging
logger = logging.getLogger('lawpal.graph')


def ensure_user_setup(*args, **kwargs):
    """ Ensures the client.ClientProfile models and setup processes get called """
    user = kwargs.get('user', None)
    request = kwargs.get('request', {})
    session = request.session if request.session else {}

    if user is None:
        logger.error('Pipeline.ensure_user_setup user is not present, cant create profile')
    else:
        # Call the lambda defined in client/models.py
        profile, is_new = _get_or_create_user_profile(user=user)

        profile.profile_data['user_class_name'] = session.get('user_class_name', 'lawyer')
        profile.save(update_fields=['profile_data'])

        create_glynt_profile(profile=profile, is_new=is_new)


def profile_extra_details(backend, details, response, user=None, is_new=False, \
                          *args, **kwargs):
    """ process the backend based on the backend type """
    if backend.name == 'linkedin':
        logger.info('Pipeline.profile_extra_details backend is linkedin')

        linkedin_profile_extra_details(backend=backend, details=details,
                                       response=response, user=user,
                                       is_new=is_new, *args, **kwargs)

    elif backend.name == 'google-oauth2':
        logger.info('Pipeline.profile_extra_details backend is google-oauth2')

        google_profile_extra_details(backend=backend, details=details,
                                       response=response, user=user,
                                       is_new=is_new, *args, **kwargs)

    else:
        logger.error('Pipeline.profile_extra_details backend is Unknown')


def get_username(details, user=None,
                 user_exists=UserSocialAuth.simple_user_exists,
                 *args, **kwargs):
    """Return an username for new user. Return current user username
    if user was given.
    """
    if user:
        logger.info('User already exists so returning them as the user: %s' % user.username)
        final_username = user.username
    else:
        uuid_length = getattr(settings, 'SOCIAL_AUTH_UUID_LENGTH', 4)
        if uuid_length <= 0:
            logger.error('uuid_length cannot be 0 or less: %d' % uuid_length)
            uuid_length = 3

        if details.get('fullname'):
            username = unicode(details['fullname'])
        elif details.get('username'):
            username = unicode(details['username'])
        else:
            username = uuid.uuid4().get_hex()

        username = slugify(username)
        logger.info('Getting username availability: %s' % username)

        max_length = UserSocialAuth.username_max_length()
        short_username = username[:max_length - uuid_length]
        final_username = UserSocialAuth.clean_username(username[:max_length])

        # Generate a unique username for current user using username
        # as base but adding a unique hash at the end. Original
        # username is cut to avoid any field max_length.

        while user_exists(username=final_username):
            logger.info('Username %s exists, trying to create another' % final_username)
            username = '%s-%s' % (short_username, uuid.uuid4().get_hex()[:uuid_length])
            username = username[:max_length]

            final_username = slugify(UserSocialAuth.clean_username(username))

        logger.info('Pipeline: username will be : %s for %s' % (final_username, user))

    return {'username': final_username}


# def ensure_mutually_exclusive_userclass(*args, **kwargs):
#     is_lawyer = False
#     request = kwargs.get('request', None)
#     opposite_user_classname = None

#     # this session var must be present as they clicked on a link that set it
#     user_class_name = request.session.get('user_class_name', None)

#     # if this user is trying to sign in as a customer
#     if user_class_name == 'customer':
#         opposite_user_classname = 'lawyer'

#     elif user_class_name == 'lawyer':
#         opposite_user_classname = 'customer'

#     # get their email, as we need to see if they are already present
#     # as a lawyer
#     email = kwargs.get('details', {"email": None})['email']

#     if email is not None:
#         # try to see if there is a user
#         try:
#             user = User.objects.filter(email=email).order_by('date_joined')[0]
#             current_user_class_name = user.profile.user_class

#         except IndexError:
#             logger.info('User is brand new no affiliation yet')
#             current_user_class_name = None

#         # oh dear class trying to log in as the opposite class
#         #import pdb;pdb.set_trace()
#         if current_user_class_name == opposite_user_classname:

#             if opposite_user_classname == 'customer':
#                 # is a customer trying to be a lawyer
#                 url = reverse('public:sorry_are_customer')

#             else:
#                 # is a lawyer trying to be a customer
#                 url = reverse('public:sorry_are_lawyer')

#             return HttpResponseRedirect(url)
#     # nothing hapened continue one
#     return None
