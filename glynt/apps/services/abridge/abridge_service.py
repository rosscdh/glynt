# -*- coding: utf-8 -*-
from abridge.services import AbridgeService
from bunch import Bunch

import logging
logger = logging.getLogger('django.request')


class LawPalAbridgeService(object):
    """
    Service to use when sending abridge events
    to the abridge service
    """
    user = None
    abridge = None
    content_group = None
    events = []

    def __init__(self, user, **kwargs):
        self.user = user
        self.abridge = AbridgeService(user=user)
        self.content_group = kwargs.get('content_group', 'General')

        logger.debug('Initialized LawPalAbridgeService')

    def add_event(self, content, **kwargs):
        """
        add our custom event object
        """

        content_group = kwargs.pop('content_group', self.content_group)
        user = kwargs.pop('user', self.user)

        user = Bunch(email=user.email, first_name=user.first_name, last_name=user.last_name)

        event = Bunch({
            'user': user,
            'content_group': content_group,
            'content': content,
            'data': kwargs
        })

        self.events.append(event)
        logger.debug('Added event {content_group}'.format(content_group=content_group))

    def send(self):
        """
        process our events and send to abridge service
        """
        logger.debug('Sending accumulated LawPalAbridgeService events')
        if self.events:

            for e in self.events:
                logger.debug('content_group: {content_group} user: {user}'.format(content_group=e.content_group, user=e.user.email))
                self.abridge.create_event(content_group=e.content_group,
                                          content=e.content,
                                          user=e.user,
                                          **e.data)
            # reset
            self.events = []