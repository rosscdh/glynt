# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.defaultfilters import slugify

from social_auth.models import UserSocialAuth
from tasks import collect_user_fullcontact_info, collect_user_graph_connections

from glynt.apps.graph.services import LinkedinProfileService
from urlparse import parse_qs

import uuid

import logging
logger = logging.getLogger('lawpal.graph')


def ensure_user_setup(*args, **kwargs):
    """ Ensures the client.ClientProfile models and setup processes get called """
    user = kwargs.get('user', None)

    if user is not None:
        # Call the lambda defined in client/models.py
        user.profile


def linkedin_profile_extra_details(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    """ see if the details dict has the linkedin picture-url or the headline
    then update the profile dictionary, which then updates the user profile
    if not present? then init the linkedinprofileservice and get it from linked in"""
    if backend.name == 'linkedin':
        profile = {}

        logger.info('Pipeline.linkedin.profile_photo logged in with linkedin')

        if details.get('headline', None) is not None:
            profile.update({
                'summary': details.get('headline')
            })

        if details.get('picture-url', None) is not None:
            profile.update({
                'photo_url': details.get('picture-url')
            })
            logger.info('Pipeline.linkedin.profile_photo details already had linkedin photo: %s' % profile.get('photo_url'))

        if details.get('summary', None) is not None:
            profile.update({
                'bio': details.get('summary')
            })
            logger.info('Pipeline.linkedin.bio details already had linkedin summary-bio')

        if user is not None:
            auth = user.social_auth.get(provider='linkedin')
            access_token = auth.extra_data.get('access_token', None)
            # get profile
            client_profile = user.profile

            if access_token is not None:
                logger.info('Pipeline.linkedin.profile_photo user: %s' % user)

                api_data = parse_qs(access_token)
                service = LinkedinProfileService(uid=auth.uid, oauth_token=api_data.get('oauth_token')[0], \
                                                    oauth_token_secret=api_data.get('oauth_token_secret')[0])
                profile = service.profile

            # logging info
            if not profile.get('photo_url'):
                logger.info('Pipeline.linkedin.photo_url user does not have linkedin photo: %s' % user)
            else:
                logger.info('Pipeline.linkedin.photo_url user %s has linkedin photo: %s' % (user, profile.get('photo_url')))
            if not profile.get('summary'):
                logger.info('Pipeline.linkedin.summary user does not have linkedin headline: %s' % user)
            else:
                logger.info('Pipeline.linkedin.summary user %s has linkedin headline: %s' % (user, profile.get('headline')))
            if not profile.get('bio'):
                logger.info('Pipeline.linkedin.bio user does not have linkedin bio: %s' % user)
            else:
                logger.info('Pipeline.linkedin.bio user %s has linkedin bio: %s' % (user, profile.get('bio')))

            if profile.get('photo_url'):
                client_profile.profile_data.update({
                    'linkedin_photo_url': profile.get('photo_url')
                })

            # Update the user summary and if a lawyer save as sumamry
            if profile.get('summary'):
                # try to save the lawyer info
                try:
                    user.lawyer_profile.summary = profile.get('summary')
                    user.lawyer_profile.save(update_fields['summary'])
                except:
                    logger.error('Pipeline.linkedin.summary could not save lawyer profile summary: %s' % user)

                client_profile.profile_data.update({
                    'linkedin_headline': profile.get('summary')
                })

            # Update the user bio from the linkedin sumamry field
            if profile.get('bio'):
                # try to save the lawyer info
                try:
                    user.lawyer_profile.bio = profile.get('bio')
                    user.lawyer_profile.save(update_fields['bio'])
                except:
                    logger.error('Pipeline.linkedin.bio could not save lawyer profile bio: %s' % user)

                client_profile.profile_data.update({
                    'linkedin_headline': profile.get('summary')
                })
            # save all updated fields
            client_profile.save(update_fields=['profile_data'])


def graph_user_connections(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    logger.debug('Graph.graph_user_connections start')
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