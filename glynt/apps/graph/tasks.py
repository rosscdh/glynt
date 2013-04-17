# -*- coding: utf-8 -*-
""" Tasks related to the Lawpal Graphing System """
from django.conf import settings

from celery.task import task

from django.core.management import call_command

import logging
logger = logging.getLogger('lawpal.graph')


@task()
def collect_user_graph_connections(auth, **kwargs):
    """ task used to initiate the collection of a users
    graph connections form the backend bassed in via auth
    """
    call_command('graph_contacts', auth=auth)