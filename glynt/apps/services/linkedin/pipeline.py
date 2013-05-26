# -*- coding: utf-8 -*-
from glynt.apps.graph.services import LinkedinProfileService
from urlparse import parse_qs

import logging
logger = logging.getLogger('lawpal.graph')


def linkedin_profile_extra_details(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    """ see if the details dict has the linkedin picture-url or the headline
    then update the profile dictionary, which then updates the user profile
    if not present? then init the linkedinprofileservice and get it from linked in"""
    profile = {}

    logger.info('Pipeline.profile_photo logged in with linkedin')

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
            if not user.lawyer_profile.summary:
                # try to save the lawyer info
                try:
                    user.lawyer_profile.summary = profile.get('summary')
                    user.lawyer_profile.save(update_fields=['summary'])
                except:
                    logger.error('Pipeline.linkedin.summary could not save lawyer profile summary: %s' % user)

            client_profile.profile_data.update({
                'linkedin_summary': profile.get('summary')
            })

        # Update the user bio from the linkedin sumamry field
        if profile.get('bio'):
            if not user.lawyer_profile.bio:
                # try to save the lawyer info
                try:
                    user.lawyer_profile.bio = profile.get('bio')
                    user.lawyer_profile.save(update_fields=['bio'])
                except:
                    logger.error('Pipeline.linkedin.bio could not save lawyer profile bio: %s' % user)

            client_profile.profile_data.update({
                'linkedin_bio': profile.get('bio')
            })

        # save all updated fields
        client_profile.save(update_fields=['profile_data'])