# -*- coding: utf-8 -*-
from django.conf import settings

from social_auth.models import UserSocialAuth
from tasks import collect_user_fullcontact_info, collect_user_graph_connections

import logging
logger = logging.getLogger('lawpal.graph')


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
