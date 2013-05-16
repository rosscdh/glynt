# -*- coding: utf-8 -*-
""" Tasks related to the Lawpal Graphing System """
from django.conf import settings

from celery.task import task

from django.core.management import call_command

import logging
logger = logging.getLogger('lawpal.graph')


@task()
def collect_user_fullcontact_info(user, **kwargs):
    """ task used to initiate the collection of a users
    full_contact data which is based on their email
    """
    logger.info('Calling graph_fullcontact_user command %s' % user)
    try:
        # call the CLI command
        call_command('graph_fullcontact_user', pk=user.pk)
    except Exception, e:
        logger.info('Failed, so retry calling graph_fullcontact_user command %s' % user)
        # add auth to the kwargs, as we handle it seperately in the signature
        kwargs.update({'pk': user.pk})
        # retry calling this same method again in 2 hours
        collect_user_fullcontact_info.retry(args=[], exc=e, countdown=7200, kwargs=kwargs)


@task()
def collect_user_graph_connections(auth, **kwargs):
    """ task used to initiate the collection of a users
    graph connections from the backend passed in via the auth
    """
    logger.info('Calling graph_contacts command %s' % auth)
    try:
        # call the CLI command
        call_command('graph_contacts', auth=auth)
    except Exception, e:
        logger.info('Failed, so retry calling collect_user_graph_connections command %s' % auth.user)
        # add auth to the kwargs, as we handle it seperately in the signature
        kwargs.update({'auth': auth})
        # retry calling this same method again in 2 hours
        collect_user_graph_connections.retry(args=[], exc=e, countdown=7200, kwargs=kwargs)