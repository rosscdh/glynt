# -*- coding: UTF-8 -*-
from django.conf import settings

import pusher
import json
import logging
logger = logging.getLogger('lawpal.services')

PUSHER_APP_ID = getattr(settings, 'PUSHER_APP_ID', None)
PUSHER_KEY = getattr(settings, 'PUSHER_KEY', None)
PUSHER_SECRET = getattr(settings, 'PUSHER_SECRET', None)

if PUSHER_APP_ID is None:
    raise Exception("You must specify a PUSHER_APP_ID in your local_settings.py")
if PUSHER_KEY is None:
    raise Exception("You must specify a PUSHER_KEY in your local_settings.py")
if PUSHER_SECRET is None:
    raise Exception("You must specify a PUSHER_SECRET in your local_settings.py")

PUSHER = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

class PusherPublisherService(object):
    """ Service to push data out to channels on pusher.com
    so the js lib can pick them up """
    channel = None
    event = None
    data = {}

    def __init__(self, channel, event, **kwargs):
        self.channel = channel
        self.event = event

        self.data.update({
            'event': self.event,
            'channel': self.channel
        })
        # append our core data
        self.data.update(kwargs)

        logger.info('Initialized PusherPublisherService with {data}'.format(data=json.dumps(self.data)))

        self.pusher = PUSHER

    def process(self, **kwargs):
        logger.info('Sending pusher event on #{channel}'.format(channel=self.channel))

        self.data.update(kwargs)
        self.pusher[self.channel].trigger(self.event, self.data)
