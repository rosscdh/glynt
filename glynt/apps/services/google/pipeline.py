# -*- coding: utf-8 -*-
from urlparse import parse_qs

import logging
logger = logging.getLogger('lawpal.services')


def google_profile_extra_details(backend, details, response, user=None, is_new=False,
                        *args, **kwargs):
    """ get the google plus profile for this user if exists """
    profile = {}

    logger.info('Pipeline logging in with google-oauth2')

    if user is not None:
        client_profile = user.profile
        # save all updated fields
        if isinstance(response, dict):
            logger.info('Pipeline.google updating client.profile_data from google %s - %s' % (user, response,) )

            client_profile.profile_data.update(response) 

            client_profile.save(update_fields=['profile_data'])