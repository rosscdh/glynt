# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.utils import get_namedtuple_choices


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

    def __unicode__(self):
        return u'%s (%s)' % (self.user.username, self.user.email,)

    @property
    def primary_firm(self):
        try:
            return self.firm_lawyers.prefetch_related().all()[0]
        except IndexError:
            return None

    def firm_name(self):
        try:
            primary_firm.name
        except:
            return None

    def username(self):
        return self.user.username

    def full_name(self):
        return self.user.get_full_name()

    def email(self):
        return self.user.email

    def last_login(self):
        return self.user.last_login

    def practice_locations(self):
        locations = []
        if self.data.get('practice_location_1', None) is not None:
            locations.append(self.data.get('practice_location_1'))
        if self.data.get('practice_location_2', None) is not None:
            locations.append(self.data.get('practice_location_2'))
        return locations
        
    def total_deals(self):
        total = self.data.get('volume_incorp_setup')
        return total
            
    @property
    def phone(self):
        return u'%s' % self.data.get('phone', None)

    @property
    def years_practiced(self):
        return u'%s' % self.data.get('years_practiced', 0)

    @property
    def current_geo_loc(self):
        return u'%s' % self.data.get('current_geo_loc', None)

    @property
    def twitter(self):
        return u'%s' % self.data.get('twitter', None)

    @property
    def angel_list(self):
        return u'%s' % self.data.get('angel_list', None)

    @property
    def website(self):
        return u'%s' % self.data.get('website', None)