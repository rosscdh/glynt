# -*- coding: utf-8 -*-
"""
Not Just standard django models
"""
import sys
from django.db import models
from glynt.apps.utils import get_namedtuple_choices
from jsonfield import JSONField


class LawpalBaseConnection(object):
    """ Generic Connection Provider """
    id = None
    provider = None
    full_name = None
    extra_data = None

    def __init__(self, provider, uid, **kwargs):
        self.uid = uid
        self.provider = provider
        self.extra_data = kwargs
        self.full_name = self.get_full_name_from_data()

    def get_full_name_from_data(self):
        raise Exception('Not Implemented')

    def __str__(self):
        return '%s' % self.__unicode__().encode(sys.stdout.encoding)

    def __unicode__(self):
        return self.full_name


class LinkedinConnection(LawpalBaseConnection):
    """ Linkedin Connection Provider """
    def get_full_name_from_data(self):
        return u'%s %s' % (self.extra_data.get('firstName'), self.extra_data.get('lastName'),)


class AngelConnection(LawpalBaseConnection):
    """ Linkedin Connection Provider """
    def get_full_name_from_data(self):
        return u'%s' % self.extra_data.get('name')


class GraphConnection(models.Model):
    """ Generic Database Model to store various provider abstractions """
    PROVIDERS = get_namedtuple_choices('PROVIDERS', (
        (0,'linkedin','Linkedin'),
        (1,'aangel','Angel'),
      
    ))
    provider = models.IntegerField(choices=PROVIDERS.get_choices(), db_index=True)
    full_name = models.CharField(max_length=128)
    extra_data = JSONField(blank=True, null=True)