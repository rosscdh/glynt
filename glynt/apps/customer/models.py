# -*- coding: UTF-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from glynt.apps.company.models import Company

from jsonfield import JSONField

import os
import logging
logger = logging.getLogger('django.request')


def _customer_upload_photo(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'customer/%s%s' % (instance.user.username, ext)


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
    photo = models.ImageField(upload_to=_customer_upload_photo)

    def __unicode__(self):
        return u'%s' % (self.user.get_full_name(),)

    def get_absolute_url(self):
        return reverse('customer:customer_profile', kwargs={'slug': self.user.username})

    @property
    def full_name(self):
        return u'%s %s' % (self.data.get('first_name', ''), self.data.get('last_name', ''), )

    @property
    def profile_photo(self):
        return self.user.profile.get_mugshot_url()

    @property
    def phone(self):
        return self.data.get('telephone', '123123123')

    @property
    def companies(self):
        return self.user.companies.all()

    @property
    def primary_company(self):
        try:
            return self.companies[0]
        except IndexError:
            # not found so return an empty instance
            return Company()
