# coding: utf-8
import os
from django.template.defaultfilters import slugify
from .models import Startup, Founder

import logging
logger = logging.getLogger('lawpal.services')


class EnsureFounderService(object):
    """ Set up a startup founder """
    founder = None

    def __init__(self, user, **kwargs):
        self.user = user
        self.summary = kwargs.pop('summary', None)
        self.bio = kwargs.pop('bio', None)
        self.photo = kwargs.pop('photo', None)
        self.data = kwargs

    def user_info(self):
        self.data['first_name'] = self.data.get('first_name', self.user.first_name)
        self.data['last_name'] = self.data.get('last_name', self.user.last_name)

    def update_user_profile(self):
        # update the is_founder attribute
        profile = self.user.profile
        profile.profile_data['is_founder'] = True
        profile.save(update_fields=['profile_data'])

    def save_photo(self, photo):
        if photo and self.founder.photo != photo: # only if its not the same image
            logger.info('New photo for %s' % self.founder)
            photo_file = os.path.basename(self.photo.file.name)# get base name
            try:
                self.founder.photo.save(photo_file, photo.file)
                self.founder.user.profile.mugshot.save(photo_file, photo.file)
                logger.info('Saved new photo %s for %s' % (photo.file, self.founder))
            except Exception as e:
                logger.error('Could not save user photo %s for %s: %s' % (photo.file, self.founder, e))

    def process(self):
        self.founder, is_new = Founder.objects.get_or_create(user=self.user)
        logger.info("Processing founder %s (is_new: %s)" % (self.user.get_full_name(), is_new,))

        self.user_info()

        if self.summary:
            self.founder.summary = self.summary

        if self.bio:
            self.founder.bio = self.bio

        if self.data:
            self.founder.data = self.data

        if self.photo:
            # pop so it does not get serialized
            self.save_photo(self.photo)

        logger.info("Saving founder %s", self.user)
        self.founder.save()
        return self.founder


class EnsureStartupService(object):
    """ Set up a startup """
    founder = None
    startup = None

    def __init__(self, name, founder=None, **kwargs):
        self.startup_name = name
        self.founder = founder
        self.slug = kwargs.pop('slug', None)
        self.summary = kwargs.pop('summary', None)
        self.website = kwargs.pop('website', None)
        self.twitter = kwargs.pop('twitter', None)
        self.photo = kwargs.pop('photo', None)
        self.data = kwargs

    def add_founder(self, founder=None):
        if self.founder or founder:
            founder = founder if founder else self.founder
            if not self.startup:
                raise Exception('Startup has not yet been defined for service, need to call .process()')

            self.startup.founders.remove(founder.user) # ensure he is not already assocaited with the startup
            self.startup.founders.add(founder.user)

    def process(self):
        self.startup, is_new = Startup.objects.get_or_create(name=self.startup_name)
        logger.info("Processing startup %s (is_new: %s)" % (self.startup, is_new,))

        self.add_founder(self.founder)

        if self.slug or is_new:
            self.startup.slug = self.slug if self.slug else slugify(self.startup_name)

        if self.summary:
            self.startup.summary = self.summary

        if self.website:
            self.startup.website = self.website

        if self.twitter:
            self.startup.twitter = self.twitter

        if self.data:
            self.startup.data = self.data

        logger.info("Saving startup %s", self.startup_name)
        self.startup.save()
        return self.startup
