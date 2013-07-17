# -*- coding: UTF-8 -*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from autoslug.fields import AutoSlugField
from jsonfield import JSONField

from glynt.apps.lawyer.models import Lawyer

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

    def __unicode__(self):
        return u'%s' % (self.name,)

    @property
    def num_offices(self):
        return 0 #self.office_set.count()

    @property
    def primary_office(self):
        try:
            return self.office_set.all()[0]
        except:
            return None


@receiver(post_save, sender=Firm, dispatch_uid='firm.new_firm', )
def new_firm(sender, **kwargs):
    """ Capture the new Firm Creation """
    firm = kwargs.get('instance', None)
    is_new = kwargs.get('created', None)

    if firm is not None and is_new == True:
        logger.info('A new Firm was created %s' % firm)
        new_firm_email_task(firm=firm)
