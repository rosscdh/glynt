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

import datetime

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

    def close(self, actioning_user):
        recipient = self.founder.user if actioning_user.profile.is_lawyer else self.lawyer.user

        self.engagement_status = ENGAGEMENT_STATUS.closed
        self.save(update_fields=['engagement_status'])

        # send notification
        description = '%s (%s) closed the Engagement' % (actioning_user.profile.non_specific_title, actioning_user)
        notify.send(actioning_user, recipient=recipient, verb=u'closed', action_object=self,
                    description=description, target=self, engagement_pk=self.pk, closed_by=actioning_user, directed_at=recipient, lawyer_pk=self.lawyer.user.pk, founder_pk=self.founder.user.pk, date_closed=datetime.datetime.utcnow())
        # Log activity to stream
        user_streams.add_stream_item(recipient, description, engagement)
        user_streams.add_stream_item(actioning_user, description, engagement)

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


# import signals so they load on django load
from signals import save_engage_comment_signal