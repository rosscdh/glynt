# coding: utf-8
import os
from django.template.defaultfilters import slugify
from .models import Startup

import logging
logger = logging.getLogger('lawpal.services')


class EnsureStartupService(object):
    """ Set up a startup """

    def __init__(self, name, **kwargs):
        self.startup_name = name
        self.slug = kwargs.pop('slug', None)
        self.summary = kwargs.pop('summary', None)
        self.website = kwargs.pop('website', None)
        self.twitter = kwargs.pop('twitter', None)
        self.photo = kwargs.pop('photo', None)
        self.data = kwargs

    def process(self):
        self.startup, is_new = Startup.objects.get_or_create(name=self.startup_name)

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

        self.startup.save()
