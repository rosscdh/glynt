# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import naturaltime
from abridge.services import AbridgeService
from abridge.services import CardService


from bunch import Bunch

import datetime
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
        self.events = []
        self.content_group = kwargs.get('content_group', 'General')

        self.check_user = kwargs.get('check_user', False)
        self.abridge = AbridgeService(user=user, check_user=self.check_user)

        logger.debug('Initialized LawPalAbridgeService')

    def append_card(self, content, **kwargs):
        logger.debug('Trying to append card to event.kwargs')

        try:
            date = datetime.datetime.utcnow()

            card_kwargs = {
                'url': kwargs.get('url', False),
                'profile_photo': kwargs.get('profile_photo', False),
                'event_date': date,
                'natural_event_date': naturaltime(date),
            }

            card_service = CardService(content=content, **card_kwargs)

            logger.debug('Successfully appended card to event.kwargs')

            # send our card through
            return card_service.card()

        except Exception as e:
            logger.error('Caught Abridge Card Exception: %s' % e)
            return None

    def add_event(self, content, **kwargs):
        """
        add our custom event object
        """

        content_group = kwargs.pop('content_group', self.content_group)
        user = kwargs.pop('user', self.user)

        user = Bunch(email=user.email, first_name=user.first_name, last_name=user.last_name)

        card = self.append_card(content=content, **kwargs)
        if card is not None:
            # if we have a card then return it and use it in the data
            kwargs.update({
                'card': card,
            })

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
