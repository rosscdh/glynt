# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from jsonfield import JSONField
from glynt.apps.utils import get_namedtuple_choices

from glynt.apps.startup.models import Startup, Founder
from glynt.apps.lawyer.models import Lawyer

from bunches import StartupEngageLawyerBunch
from managers import DefaultEngageManager

from utils import *
ENGAGEMENT_STATUS = get_namedtuple_choices('ENGAGEMENT_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'closed', 'Closed'),
))


class Engagement(models.Model):
    """ Base Engagement object
    Stores initial engagement details
    """
    engagement_status = models.IntegerField(choices=ENGAGEMENT_STATUS.get_choices(), default=ENGAGEMENT_STATUS.new, db_index=True)
    startup = models.ForeignKey(Startup)
    founder = models.ForeignKey(Founder)
    lawyer = models.ForeignKey(Lawyer)
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    objects = DefaultEngageManager()

    def __unicode__(self):
        return '%s (%s) enagement of %s' % (self.startup, self.founder, self.lawyer,)

    def get_absolute_url(self):
        return reverse('engage:engagement', kwargs={'pk':self.pk})

    @property
    def status(self):
        return ENGAGEMENT_STATUS.get_desc_by_value(self.engagement_status)

    @property
    def engagement_statement(self):
        return self.data.get('engagement_statement', None)

    @property
    def engagement_types(self):
        engagement_types = [('engage_for_general','General'), ('engage_for_incorporation','Incorporation'), ('engage_for_ip','Intellectual Property'), ('engage_for_employment','Employment Law'), ('engage_for_fundraise','Fundraising'), ('engage_for_cofounders','Co-Founder')]
        return [(self.data.get(r,False),name) for r,name in engagement_types if self.data.get(r,False)]
