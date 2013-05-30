# coding: utf-8
import os
from django.db import models
from django.contrib.auth.models import User

from autoslug.fields import AutoSlugField
from jsonfield import JSONField


def _startup_upload_photo(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'startup/%s%s' % (instance.slug, ext)


def _founder_upload_photo(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'founder/%s%s' % (instance.user.username, ext)


class Startup(models.Model):
    """ The Startups
    Stores various information related to startups,
    including relationships to founders (Users)
    """
    name = models.CharField(max_length=255, db_index=True)
    slug = AutoSlugField(db_index=True, populate_from='name', editable=True)
    summary = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(upload_to=_startup_upload_photo)
    founders = models.ManyToManyField(User, related_name='startups')
    data = JSONField(default={})

    def __unicode__(self):
        return self.name


class Founder(models.Model):
    """ The founders
    Founders might be the best word choice. Think
    of this as a profile for a User involved in startup
    activity.
    """
    user = models.OneToOneField(User, related_name='founder_profile')
    summary = models.CharField(max_length=255)
    bio = models.TextField()
    data = JSONField(default={})
    photo = models.ImageField(upload_to=_founder_upload_photo)

    def __unicode__(self):
        return self.user.username

    @property
    def profile_photo(self):
        return self.user.profile.get_mugshot_url()

    @property
    def startups(self):
        return self.user.startups.all()

    @property
    def primary_startup(self):
        try:
            return self.startups[0]
        except IndexError:
            # not found so return an empty instance
            return Startup()
