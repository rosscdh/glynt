# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.utils import get_namedtuple_choices

from glynt.apps.startup.models import Startup, Founder
from glynt.apps.lawyer.models import Lawyer


ENGAGEMENT_STATUS = get_namedtuple_choices('ENGAGEMENT_STATUS', (
    (0, 'requested', 'Requested'),
    (1, 'considering', 'Lawyer has recieved the request and is considering it'),
    (2, 'engaged', 'Engaged'),
    (3, 'paused', 'Engagement Paused'),
    (4, 'complete', 'Completed Engagement'),
))


class Engagement(models.Model):
    """ Base Engagement object
    Stores initial engagement details
    """
    engagement_status = models.IntegerField(choices=ENGAGEMENT_STATUS.get_choices(), default=ENGAGEMENT_STATUS.requested, db_index=True)
    startup = models.ForeignKey(Startup)
    founder = models.ForeignKey(Founder)
    lawyer = models.ForeignKey(Lawyer)
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return '%s (%s) enagement of %s' % (self.startup, self.founder, self.lawyer,)

    @property
    def status(self):
        return ENGAGEMENT_STATUS.get_desc_by_value(self.engagement_status)

    def engagement_statement(self):
        return self.data.get('engagement_statement', None)