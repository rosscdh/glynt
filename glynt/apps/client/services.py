# -*- coding: UTF-8 -*-
from django.conf import settings
from glynt.apps.graph.models import FullContactData

from glynt.apps.company.bunches import UserIntakeCompanyBunch
from glynt.apps.company.forms import CompanyProfileForm

import logging
logger = logging.getLogger('lawpal.services')


class EnsureUserHasCompletedIntakeProcess(object):
    """ Service used to test if the user has completed the intake form """
    has_completed_intake = False
    user = None
    profile = None

    def __init__(self, user):
        self.user = user
        self.profile = self.user.profile
        self.process()

    def is_complete(self):
        return self.has_completed_intake

    def process(self):
        bunch = UserIntakeCompanyBunch(user=self.user)
        form = CompanyProfileForm(bunch.get_data_bag())
        self.has_completed_intake = form.is_valid()
        return self.has_completed_intake

    


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

        self.fc, is_new = FullContactData.objects.get_or_create(user=user)
        logger.info('FullContact model for: %d is_new: %s' % (user.pk, is_new))

        self.data = self.fc.extra_data

        self.process()

    def photo(self):
        """ update photo only if the user has not entered data """
        #logger.debug('FC: current bio: %s' % self.user.profile.mugshot.file)
        if self.user.profile.mugshot in [None,'']:
            self.user.profile.mugshot = self.fc.primary_photo_url
            self.user.profile.save(update_fields=['mugshot'])
            logger.info('FC: set the user profile mugshot: %d' % self.user.pk)

    def twitter(self):
        if self.user.lawyer_profile.data.get('twitter', None) is None or len(self.user.lawyer_profile.data.get('twitter')) == 0:
            for p in self.fc.profiles():
                if p.get('typeId',None) == 'twitter' and p.get('username', None) is not None:
                    self.user.lawyer_profile.data['twitter'] = p.get('username')
                    self.user.lawyer_profile.save(update_fields=['data'])
                    break

    def bio(self):
        """ update bio only if the user has not entered data """
        #logger.debug('FC: current summary: %s' % self.user.lawyer_profile.summary)
        if len(self.user.lawyer_profile.bio.strip()) == 0:

            b = self.fc.primary_profile.get('bio', None) # get from model property

            if b is not None:
                self.user.lawyer_profile.bio = b
                self.user.lawyer_profile.save(update_fields=['bio'])
                logger.info('FC: set the user bio: %d' % self.user.pk)


    def process(self):
        self.photo()
        self.twitter()
        self.bio()
