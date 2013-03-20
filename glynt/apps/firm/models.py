# -*- coding: UTF-8 -*-
from django.db import models

from jsonfield import JSONField


class tmpLawyerFirm(models.Model):
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