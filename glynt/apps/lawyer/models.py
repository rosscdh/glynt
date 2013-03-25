# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.utils import get_namedtuple_choices


class Lawyer(models.Model):
    """ The Firms
    Stores sundry information about legal Firms
    """
    LAWYER_ROLES = get_namedtuple_choices('LAWYER_ROLES', (
        (1, 'role1', 'Role 1'),
        (2, 'role2', 'Role 2'),
        (3, 'role3', 'Role 3'),
    ))
    user = models.ForeignKey(User)
    role = models.IntegerField(choices=LAWYER_ROLES.get_choices(), db_index=True)
    summary = models.CharField(max_length=255)
    bio = models.TextField()
    data = JSONField()
    photo = models.ImageField(upload_to='lawyer')

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