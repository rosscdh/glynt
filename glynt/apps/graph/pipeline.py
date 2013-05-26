# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.defaultfilters import slugify

from social_auth.models import UserSocialAuth
from tasks import collect_user_fullcontact_info, collect_user_graph_connections

from glynt.apps.client.models import _create_user_profile, create_glynt_profile
from glynt.apps.services.linkedin.pipeline import linkedin_profile_extra_details
from urlparse import parse_qs

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
        profile, is_new = _create_user_profile(user=user)

        profile.profile_data['user_class_name'] = session.get('user_class_name', 'lawyer')
        profile.save(update_fields=['profile_data'])

        create_glynt_profile(profile=profile, is_new=is_new)


def profile_extra_details(backend, details, response, user=None, is_new=False, \
                        *args, **kwargs):
    """ process the backend based on the backend type """
    if backend.name == 'linkedin':
        logger.info('Pipeline.profile_photo backend is linkedin')

        linkedin_profile_extra_details(backend, details, response, user=None, is_new=False, \
                        *args, **kwargs)

    elif backend.name == 'google-oauth2':
        logger.info('Pipeline.profile_photo backend is google-oauth2')

    else:
        logger.info('Pipeline.profile_photo backend is not linkedin')


def graph_user_connections(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    logger.debug('Graph.graph_user_connections start')

    if getattr(settings, 'BROKER_BACKEND', None): # only do this if we have a broker
        if user is not None:

            auth = UserSocialAuth.objects.get(user=user, provider=backend.name)
            logger.info('Pipeline: Graph.graph_user_connections auth: %s' % auth)

            try:
                logger.info('Pipeline: Graph.collect_user_fullcontact_info auth: %s' % user)
                collect_user_fullcontact_info.delay(user=user)
            except Exception as e:
                logger.error('Did not try collect_user_fullcontact_info as no connection to broker could be found: %s' % e)

            try:
                logger.info('Pipeline: Graph.collect_user_graph_connections auth: %s' % user)
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
        logger.info('User exists: %s' % user.username)
        return {'username': user.username}

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


    return {'username': final_username}