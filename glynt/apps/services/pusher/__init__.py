# -*- coding: UTF-8 -*-
from django.conf import settings
from celery.task import task

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


if not settings.IS_TESTING:
    PUSHER_CLIENT = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)
else:
    PUSHER_CLIENT = None

@task()
def _send(channel, event, data):
    if PUSHER_CLIENT is not None:
        PUSHER_CLIENT[channel].trigger(event, data)


class PusherPublisherService(object):
    """ Service to push data out to channels on pusher.com
    so the js lib can pick them up """
    channels = None
    event = None
    data = {}

    def __init__(self, channel, event, **kwargs):
        # is we pass in a tuple or list (iterable)
        # otherwise make it a list
        self.channels =  channel if hasattr(channel, '__iter__') else [channel]
        self.event = event

        # append our core data
        self.data.update(kwargs)

        logger.debug('Initialized PusherPublisherService with {data}'.format(data=json.dumps(self.data)))


    def process(self, **kwargs):
        if not settings.IS_TESTING:

            if 'event' not in kwargs:
                kwargs.update({'event': self.event})

            self.data.update(kwargs)

            for channel in self.channels:
                logger.debug('Sending pusher event on #{channel}'.format(channel=channel))

                self.data.update({
                    'channel': channel,
                })

                try:
                    _send.delay(channel=channel, event=self.event, data=self.data)
                except Exception as e:
                    # call normally
                    logger.error('PusherPublisherService _send.delay could not be called (celery): %s' % e)
                    _send(channel=channel, event=self.event, data=self.data)
