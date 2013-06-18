# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from jsonfield import JSONField

from glynt.utils import generate_unique_slug
from glynt.apps.engage import ENGAGEMENT_STATUS
from glynt.apps.engage.services.actions import OpenEngagementService, CloseEngagementService, ReOpenEngagementService
from glynt.apps.startup.models import Startup, Founder
from glynt.apps.lawyer.models import Lawyer

from managers import DefaultEngagementManager




class Engagement(models.Model):
    """ Base Engagement object
    Stores initial engagement details
    NB, slug is generated on save if it is not set
    """
    engagement_status = models.IntegerField(choices=ENGAGEMENT_STATUS.get_choices(), default=ENGAGEMENT_STATUS.new, db_index=True)
    slug = models.SlugField(max_length=128, blank=False)
    startup = models.ForeignKey(Startup)
    founder = models.ForeignKey(Founder)
    lawyer = models.ForeignKey(Lawyer)
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    objects = DefaultEngagementManager()

    def __unicode__(self):
        return '%s of %s Enagement with %s' % (self.founder.user.get_full_name(), self.startup, self.lawyer.user.get_full_name(),)

    def get_absolute_url(self):
        return reverse('engage:engagement', kwargs={'slug': self.slug})

    def open(self, actioning_user):
        """ Open the notification """
        service = OpenEngagementService(engagement=self, actioning_user=actioning_user)
        return service.process()

    def close(self, actioning_user):
        service = CloseEngagementService(engagement=self, actioning_user=actioning_user)
        return service.process()

    def reopen(self, actioning_user):
        service = ReOpenEngagementService(engagement=self, actioning_user=actioning_user)
        return service.process()

    @property
    def is_open(self):
        return ENGAGEMENT_STATUS.open == self.engagement_status

    @property
    def is_closed(self):
        return ENGAGEMENT_STATUS.closed == self.engagement_status

    @property
    def is_new(self):
        return ENGAGEMENT_STATUS.new == self.engagement_status

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

    def save(self, *args, **kwargs):
        """ Ensure that we have a slug """
        if self.slug in [None, '']:
            self.slug = generate_unique_slug(instance=self)

        return super(Engagement, self).save(*args, **kwargs)


# import signals so they load on django load
from glynt.apps.engage.signals import save_engagement_comment_signal