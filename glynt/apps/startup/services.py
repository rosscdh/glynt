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

    def process(self):
        self.founder, is_new = Founder.objects.get_or_create(user=self.user)
        logger.info("Processing founder %s (is_new: %s)" % (self.user.get_full_name(), is_new,))

        if self.summary:
            self.founder.summary = self.summary

        if self.bio:
            self.founder.bio = self.bio

        if self.photo and self.photo != self.founder.photo:
            filename = os.path.basename(self.photo.name)
            self.founder.photo.save(filename, self.photo)

        if self.data:
            self.founder.data = self.data

        logger.info("Saving founder %s", self.user)
        self.founder.save()
        return self.founder


class EnsureStartupService(object):
    """ Set up a startup """
    startup = None
    def __init__(self, name, founder, **kwargs):
        self.startup_name = name
        self.founder = founder
        self.slug = kwargs.pop('slug', None)
        self.summary = kwargs.pop('summary', None)
        self.website = kwargs.pop('website', None)
        self.twitter = kwargs.pop('twitter', None)
        self.photo = kwargs.pop('photo', None)
        self.data = kwargs

    def add_founder(self, founder):
        if not self.startup:
            raise Exception('Startup has not yet been defined for service, need to call .process()')

        self.startup.founders.remove(self.founder) # ensure he is not already assocaited with the startup
        self.startup.founders.add(self.founder)

    def process(self):
        self.startup, is_new = Startup.objects.get_or_create(name=self.startup_name)
        logger.info("Processing startup %s (is_new: %s)" % (self.startup, is_new,))

        if self.slug or is_new:
            self.startup.slug = self.slug if self.slug else slugify(self.startup_name)

        if self.summary:
            self.startup.summary = self.summary

        if self.website:
            self.startup.website = self.website

        if self.twitter:
            self.startup.twitter = self.twitter

        if self.photo and self.photo != self.startup.photo:
            filename = os.path.basename(self.photo.name)
            self.startup.photo.save(filename, self.photo)

        if self.data:
            self.startup.data = self.data

        logger.info("Saving startup %s", self.startup_name)
        self.startup.save()
        return self.startup
