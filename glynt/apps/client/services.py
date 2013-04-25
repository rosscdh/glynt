# -*- coding: UTF-8 -*-
from django.conf import settings
from glynt.apps.graph.models import FullContactData

import logging
logger = logging.getLogger('lawpal.services')


class FullContactProfileDataService(object):
    """ Populate a user based on their FullContact data
    if any provided.
    Service will loop over profile data looking for a primary=True
    if found will return the data for that profile
    """
    primary_profile = {}

    def __init__(self, user, **kwargs):
        logger.info('Populate User Profile from FullContact for: %d' % user.pk)
        self.user = user
        self.fc = FullContactData.objects.get(user=user)
        self.data = self.fc.extra_data

        self.process()

    def photo(self):
        #logger.debug('FC: current bio: %s' % self.user.profile.mugshot.file)
        if self.user.profile.mugshot in [None,'']:
            self.user.profile.mugshot = self.fc.primary_photo_url
            self.user.profile.save(update_fields=['mugshot'])
            logger.info('FC: set the user profile mugshot: %d' % self.user.pk)

    def bio(self):
        #logger.debug('FC: current summary: %s' % self.user.lawyer_profile.summary)
        if len(self.user.lawyer_profile.bio) == 0:

            b = self.fc.primary_profile.get('bio', None) # get from model property

            if b is not None:
                self.user.lawyer_profile.bio = b
                self.user.lawyer_profile.save(update_fields=['bio'])
                logger.info('FC: set the user bio: %d' % self.user.pk)


    def process(self):
        self.photo()
        self.bio()
