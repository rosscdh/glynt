# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.defaultfilters import slugify

from social_auth.models import UserSocialAuth
from tasks import collect_user_fullcontact_info, collect_user_graph_connections

import uuid

import logging
logger = logging.getLogger('lawpal.graph')


def ensure_user_setup(*args, **kwargs):
    """ Ensures the client.ClientProfile models and setup processes get called """
    user = kwargs.get('user', None)

    if user is not None:
        # Call the lambda defined in client/models.py
        user.profile



def graph_user_connections(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):

    if user is not None:
        auth = UserSocialAuth.objects.get(user=user, provider=backend.name)
        
        try:
            collect_user_fullcontact_info.delay(user=user)
        except Exception as e:
            logger.error('Did not try collect_user_fullcontact_info as no connection to broker could be found: %s' % e)

        try:
            collect_user_graph_connections.delay(auth=auth)
        except Exception as e:
            logger.error('Did not try collect_user_graph_connections as no connection to broker could be found: %s' % e)



def get_username(details, user=None,
                 user_exists=UserSocialAuth.simple_user_exists,
                 *args, **kwargs):
    """Return an username for new user. Return current user username
    if user was given.
    """
    if user:
        return {'username': user.username}

    uuid_length = getattr(settings, 'SOCIAL_AUTH_UUID_LENGTH', 4)

    if details.get('fullname'):
        username = unicode(details['fullname'])
    elif details.get('username'):
        username = unicode(details['username'])
    else:
        username = uuid.uuid4().get_hex()

    username = slugify(username)

    max_length = UserSocialAuth.username_max_length()
    short_username = username[:max_length - uuid_length]
    final_username = UserSocialAuth.clean_username(username[:max_length])

    # Generate a unique username for current user using username
    # as base but adding a unique hash at the end. Original
    # username is cut to avoid any field max_length.
    while user_exists(username=final_username):
        username = short_username + uuid.uuid4().get_hex()[:uuid_length]
        username = username[:max_length]
        final_username = slugify(UserSocialAuth.clean_username(username))

    return {'username': final_username}