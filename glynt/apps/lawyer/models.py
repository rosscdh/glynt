# -*- coding: UTF-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.utils import get_namedtuple_choices

from managers import DefaultLawyerManager, ApprovedLawyerManager

import logging
logger = logging.getLogger('django.request')


class Lawyer(models.Model):
    """ The Firms
    Stores sundry information about legal Firms
    LAWYER_ROLES: discussed and was very sure that lawyers only have 1 role
    and are never part of more than 1 firm
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
    photo = models.ImageField(upload_to='lawyer', blank=True)
    is_active = models.BooleanField(default=False, db_index=True)

    objects = DefaultLawyerManager()
    approved = ApprovedLawyerManager()

    def __unicode__(self):
        return u'%s (%s)' % (self.user.username, self.user.email,)

    @property
    def primary_firm(self):
        try:
            return self.firm_lawyers.all().prefetch_related()[0]
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
            try:
                return self.user.profile.profile_data.get('linkedin_photo_url', None) or self.user.profile.get_mugshot_url()
            except:
                return getattr(settings, 'USERENA_MUGSHOT_DEFAULT', '') # must return string here if no mugshot default


    def username(self):
        return self.user.username

    def full_name(self):
        return self.user.get_full_name()

    def email(self):
        return self.user.email

    def last_login(self):
        return self.user.last_login

    @property
    def search_locations(self):
        return ', '.join(self.practice_locations())

    def practice_locations(self):
        locations = []
        if self.data.get('practice_location_1', None) is not None:
            locations.append(self.data.get('practice_location_1'))
        if self.data.get('practice_location_2', None) is not None:
            locations.append(self.data.get('practice_location_2'))
        return locations

    @property
    def startups_advised(self):
        try:
            return self.data.get('startups_advised', [])
        except:
            return []

    @property
    def total_deals(self):
        return self.data.get('volume_incorp_setup', 0)
            
    @property
    def phone(self):
        return u'%s' % self.data.get('phone', None)

    @property
    def years_practiced(self):
        return u'%s' % self.data.get('years_practiced', 0)

    @property
    def geo_loc(self):
        return self.data.get('current_geo_loc', None)

    @property
    def twitter(self):
        return u'%s' % self.data.get('twitter', None)

    @property
    def angel_list(self):
        return u'%s' % self.data.get('angel_list', None)

    @property
    def website(self):
        return u'%s' % self.data.get('website', None)

    @property
    def seed_financing_amount_min(self):
        return u'%s' % self.data.get('seed_financing_amount_min', None)

    @property
    def seed_financing_amount_max(self):
        return u'%s' % self.data.get('seed_financing_amount_max', None)

    @property
    def seed_fee_cap_available(self):
        return u'%s' % self.data.get('seed_fee_cap_available', None)

    @property
    def seed_deferred_fees_available(self):
        return u'%s' % self.data.get('seed_deferred_fees_available', None)

    @property
    def seed_fixed_fees_available(self):
        return u'%s' % self.data.get('seed_fixed_fees_available', None)

    @property
    def incorporation_min(self):
        return u'%s' % self.data.get('seed_financing_amount_min', None)

    @property
    def incorporation_max(self):
        return u'%s' % self.data.get('seed_financing_amount_max', None)

    @property
    def inc_fee_cap_available(self):
        return u'%s' % self.data.get('inc_fee_cap_available', None)

    @property
    def inc_deferred_fees_available(self):
        return u'%s' % self.data.get('inc_deferred_fees_available', None)

    @property
    def inc_fixed_fees_available(self):
        return u'%s' % self.data.get('inc_fixed_fees_available', None)
