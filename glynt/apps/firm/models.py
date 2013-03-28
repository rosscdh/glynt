# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

from glynt.apps.deal.models import Deal


class Firm(models.Model):
    """ The Firms
    Stores sundry information about legal Firms
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    summary = models.CharField(max_length=255)
    website = models.URLField()
    twitter = models.CharField(max_length=64, db_index=True)
    photo = models.ImageField(upload_to='firm')
    data = JSONField()
    lawyers = models.ManyToManyField(User, related_name='firm_lawyers')
    deals = models.ManyToManyField(Deal, related_name='firm_deals')

    def __unicode__(self):
        return u'%s' % (self.name,)

class Office(models.Model):
    """ The Firm Office
    Model provides Offices related to a Firm
    """
    firm = models.ForeignKey(Firm)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=64, db_index=True)
    photo = models.ImageField(upload_to='office')
    data = JSONField()

    def __unicode__(self):
        return u'%s - %s' % (self.firm.name, self.address,)

    @property
    def geo_location(self):
        return u'%s' % self.data.get('geo_location', None)


class tmpLawyerFirm(models.Model):
    """ Temp Table to allow capture of lawyer data"""
    data = JSONField()
    def __unicode__(self):
        return u'%s %s'% (self.full_name, self.firm,)
    @property
    def email(self):
        return '%s' % self.data.get('email', 'noone@lawpal.com')
    @property
    def full_name(self):
        return u'%s %s' % (self.data.get('first_name', None), self.data.get('last_name', None),)
    @property
    def firm(self):
        return u'%s' % self.data.get('firm', 'No Firm')