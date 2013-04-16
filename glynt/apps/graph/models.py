# -*- coding: utf-8 -*-
"""
Not standard django models
"""
import sys

class LawpalBaseConnection(object):
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
    def get_full_name_from_data(self):
        return u'%s %s' % (self.extra_data.get('firstName'), self.extra_data.get('lastName'),)


class AngelConnection(LawpalBaseConnection):
    def get_full_name_from_data(self):
        return u'%s' % self.extra_data.get('name')