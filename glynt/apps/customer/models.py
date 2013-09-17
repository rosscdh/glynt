# coding: utf-8
import os
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from glynt.apps.project.models import Project
from glynt.apps.company.models import Company

from jsonfield import JSONField

import logging
logger = logging.getLogger('django.request')


class CustomerLoginLogic(object):
    """ Login logic used to determin what to show """
    user = None
    customer = None

    def __init__(self, user):
        self.user = user
        try:
            self.customer = self.user.customer_profile
        except ObjectDoesNotExist:
            self.customer = None
            logger.error("founder profile not found for %s" % self.user)

    @property
    def url(self):
        num_projects = Project.objects.filter(customer=self.customer).count()

        if num_projects > 0:
            return reverse('dashboard:overview')
        else:
            return reverse('project:create')

    def redirect(self):
        return redirect(self.url)


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
        return u'%s' % (self.full_name,)

    def get_absolute_url(self):
        return reverse('customer:customer_profile', kwargs={'slug': self.user.username})

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
    def primary_company(self):
        try:
            return self.companies[0]
        except IndexError:
            # not found so return an empty instance
            return Company()
