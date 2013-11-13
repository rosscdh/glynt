# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from glynt.apps.utils import get_namedtuple_choices
from .managers import LawyerManager
from .transaction_packages import TransactionPackageBunch

from jsonfield import JSONField
from storages.backends.s3boto import S3BotoStorage

import os
import logging
logger = logging.getLogger('django.request')

USERENA_MUGSHOT_DEFAULT = getattr(settings, 'USERENA_MUGSHOT_DEFAULT', None)


def _lawyer_upload_photo(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'lawyer/%s-%s%s' % (instance.user.username, slugify(filename), ext)


class Lawyer(models.Model):
    """ The Firms
    Stores sundry information about legal Firms
    LAWYER_ROLES: discussed and was very sure that lawyers only have 1 role
    and are never part of more than 1 firm

    Note: we make use of __getattr__ to access data stored in the local JSONField
    i.e. just refer to it. lawyer_object.my_obtuse_variable
    If you require a specific sort of default ie.. not None
    then write a custom getter
    """
    LAWYER_ROLES = get_namedtuple_choices('LAWYER_ROLES', (
        (13, 'managing_partner', 'Managing Partner'),
        (8, 'senior_partner', 'Senior Partner'),
        (5, 'partner', 'Partner'),
        (3, 'of_counsel', 'Of Counsel'),
        (2, 'senior_associate', 'Senior Associate'),
        (1, 'associate', 'Associate'),
    ))

    user = models.OneToOneField(User, related_name='lawyer_profile')
    role = models.IntegerField(choices=LAWYER_ROLES.get_choices(), default=LAWYER_ROLES.associate, db_index=True)
    summary = models.CharField(max_length=255)
    bio = models.TextField()
    data = JSONField(default={})
    photo = models.ImageField(upload_to=_lawyer_upload_photo, blank=True, storage=S3BotoStorage())
    is_active = models.BooleanField(default=False, db_index=True)

    objects = LawyerManager()

    def __unicode__(self):
        return u'%s' % (self.user.get_full_name(),)

    def __getattr__(self, attr_name):
        """ leverage python to get the attr if its not already part of the model structure
        getatt is only called at 'finally' once all other lookup types have failed """
        if attr_name not in self.data:
            raise AttributeError(attr_name)
        return self.data.get(attr_name, None)

    def get_absolute_url(self):
        return reverse('lawyer:profile', kwargs={'slug': self.user.username})

    @property
    def primary_firm(self):
        try:
            return self.firm_lawyers.prefetch_related().all()[0]
        except IndexError:
            return None

    @property
    def firm_name(self):
        try:
            return self.primary_firm.name
        except:
            return None

    @property
    def position(self):
        return self.LAWYER_ROLES.get_desc_by_value(self.role)

    @property
    def profile_photo(self):
        try:
            return self.photo.url
        except:
            return self.user.profile.profile_data.get('linkedin_photo_url', USERENA_MUGSHOT_DEFAULT)

    def username(self):
        return self.user.username

    @property
    def full_name(self):
        full_name = u'%s %s' % (self.data.get('first_name', '').strip(), self.data.get('last_name', '').strip())
        if not full_name.strip():
            full_name = self.user.get_full_name()
        return full_name

    def email(self):
        return self.user.email

    def last_login(self):
        return self.user.last_login

    @property
    def profile_status(self):
        return u'%s' % ('live' if self.is_active is True else 'pending activation and will appear live shortly.')

    @property
    def phone(self):
        return self.data.get('phone')

    @property
    def search_locations(self):
        return ', '.join(self.practice_locations())

    def practice_locations(self):
        locations = []
        if self.data.get('practice_location_1', None) is not None:
            locations.append(self.data.get('practice_location_1'))
        if self.data.get('practice_location_2', None) is not None:
            locations.append(self.data.get('practice_location_2'))
        return [l.strip() for l in locations if l.strip() != '']

    @property
    def fee_packages(self):
        return TransactionPackageBunch(data=self.data)

    @property
    def companies_advised(self):
        try:
            return self.data.get('companies_advised', [])
        except:
            return []

    @property
    def total_deals(self):
        return self.data.get('volume_incorp_setup', 0)

    @property
    def years_practiced(self):
        return u'%s' % self.data.get('years_practiced', 0)

    @property
    def geo_loc(self):
        return self.data.get('current_geo_loc')
