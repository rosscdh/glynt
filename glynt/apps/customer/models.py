# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from glynt.apps.company.models import Company

from jsonfield import JSONField
from storages.backends.s3boto import S3BotoStorage

import os
import logging
logger = logging.getLogger('django.request')

USERENA_MUGSHOT_DEFAULT = getattr(settings, 'USERENA_MUGSHOT_DEFAULT', 'http://placehold.it/50x50')


def _customer_upload_photo(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'customer/%s-%s%s' % (instance.user.username, slugify(filename), ext)


class Customer(models.Model):
    """ The customer (currently just startup founders)
    Customers might be the best word choice. Think
    of this as a profile for a User involved in startup
    activity.
    """
    user = models.OneToOneField(User, related_name='customer_profile')
    summary = models.CharField(max_length=255)
    bio = models.TextField()
    data = JSONField(default={})
    photo = models.ImageField(upload_to=_customer_upload_photo, blank=True, storage=S3BotoStorage())

    def __unicode__(self):
        return u'%s' % (self.user.get_full_name(),)

    def get_absolute_url(self):
        return reverse('customer:customer_profile', kwargs={'slug': self.user.username})

    @property
    def full_name(self):
        return u'%s %s' % (self.data.get('first_name', ''), self.data.get('last_name', ''), )

    @property
    def profile_photo(self):
        try:
            return self.photo.url
        except:
            return self.user.profile.profile_data.get('picture', USERENA_MUGSHOT_DEFAULT)

    @property
    def phone(self):
        return self.data.get('phone', '')

    @property
    def companies(self):
        return self.user.companies.all()

    @property
    def primary_company(self):
        try:
            return self.user.companies.get(name=self.data.get('company_name'))
        except Company.DoesNotExist:
            # not found so return an empty instance
            return Company()
