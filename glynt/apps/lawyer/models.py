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
    photo = models.ImageField(upload_to='lawyer')

    def __unicode__(self):
        return u'%s' % (self.user.username,)

    @property
    def phone(self):
        return u'%s' % self.data.get('phone', None)

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