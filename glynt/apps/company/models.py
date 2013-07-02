# coding: utf-8
import os
from django.conf import settings
from django.core.urlresolvers import reverse
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


class Company(models.Model):
    """ The Companies
    Stores various information related to companies,
    including relationships to founders (Users)
    """
    name = models.CharField(max_length=255, db_index=True)
    slug = AutoSlugField(db_index=True, populate_from='name', editable=True)
    summary = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(upload_to=_startup_upload_photo)
    founders = models.ManyToManyField(User, related_name='companies')
    data = JSONField(default={})

    def __unicode__(self):
        return self.name

    @property
    def profile_photo(self):
        try:
            return self.photo if self.photo else self.founders.all()[0].profile.get_mugshot_url()
        except:
            return settings.USERENA_MUGSHOT_DEFAULT


class Founder(models.Model):
    """ The founder
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
        return u'%s' % (self.full_name,)

    def get_absolute_url(self):
        return reverse('company:founder_profile', kwargs={'slug': self.user.username})

    @property
    def full_name(self):
        return u'%s %s' % (self.data.get('first_name'), self.data.get('last_name'))

    @property
    def profile_photo(self):
        return self.user.profile.get_mugshot_url()

    @property
    def companies(self):
        return self.user.companies.all()

    @property
    def primary_startup(self):
        try:
            return self.companies[0]
        except IndexError:
            # not found so return an empty instance
            return Company()
