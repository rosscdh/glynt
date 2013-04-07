# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.deal.models import Deal


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
    photo = models.ImageField(upload_to='founder')

    def __unicode__(self):
        return self.user.username


class Startup(models.Model):
    """ The Startups
    Stores various information related to startups,
    including relationships to founders (Users)
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    summary = models.TextField()
    website = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(upload_to='startup')
    founders = models.ManyToManyField(User, related_name='startups')
    # todo: not sure about this:
    deals = models.ManyToManyField(Deal, related_name='deals')
    data = JSONField(default={})

    def __unicode__(self):
        return self.name
