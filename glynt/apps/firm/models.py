# -*- coding: UTF-8 -*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from autoslug.fields import AutoSlugField
from jsonfield import JSONField

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.deal.models import Deal

from tasks import new_firm_email_task

import logging
logger = logging.getLogger('django.request')


class Firm(models.Model):
    """ The Firms
    Stores sundry information about legal Firms
    """
    name = models.CharField(max_length=128, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True)
    summary = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=64, blank=True, db_index=True)
    photo = models.ImageField(upload_to='firm', blank=True)
    data = JSONField(default={})
    lawyers = models.ManyToManyField(Lawyer, blank=True, related_name='firm_lawyers')
    deals = models.ManyToManyField(Deal, blank=True, related_name='firm_deals')

    def __unicode__(self):
        return u'%s' % (self.name,)

    @property
    def primary_office(self):
        try:
            return self.office_set.all()[0]
        except:
            return None


class Office(models.Model):
    """ The Firm Office
    Model provides Offices related to a Firm
    """
    firm = models.ForeignKey(Firm)
    address = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=64, db_index=True, blank=True)
    photo = models.ImageField(upload_to='office', blank=True)
    data = JSONField(default={})

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


@receiver(post_save, sender=Firm, dispatch_uid='firm.new_firm', )
def new_firm(sender, **kwargs):
    """ Capture the new Firm Creation """
    firm = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if firm is not None and is_new == True:
        logger.info('A new Firm was created %s' % firm)
        new_firm_email_task(firm=firm)
