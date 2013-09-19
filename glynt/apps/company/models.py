# -*- coding: UTF-8 -*-
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from glynt.apps.company import COMPANY_STATUS_CHOICES

from autoslug.fields import AutoSlugField
from jsonfield import JSONField


def _startup_upload_photo(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'company/%s%s' % (instance.slug, ext)


class Company(models.Model):
    """ The Companies
    Stores various information related to companies,
    including relationships to customer
    """
    name = models.CharField(max_length=255, db_index=True)
    slug = AutoSlugField(db_index=True, populate_from='name', editable=True)
    summary = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(upload_to=_startup_upload_photo)
    customers = models.ManyToManyField(User, related_name='companies')
    data = JSONField(default={})

    def __unicode__(self):
        return self.name

    @property
    def status(self):
        return COMPANY_STATUS_CHOICES.get_desc_by_value(self.data.current_status)

    @property
    def profile_photo(self):
        try:
            return self.photo if self.photo else self.customers.all()[0].profile.get_mugshot_url()
        except:
            return settings.USERENA_MUGSHOT_DEFAULT
