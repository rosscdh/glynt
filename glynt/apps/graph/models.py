# -*- coding: utf-8 -*-
"""
Not Just standard django models
"""
import sys
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from glynt.apps.utils import get_namedtuple_choices
from jsonfield import JSONField

import logging
logger = logging.getLogger('lawpal.graph')


class FullContactData(models.Model):
    """ Provides a data source for a users fullcontact.com info """
    user = models.ForeignKey(User)
    extra_data = JSONField(blank=True, default={})

    def photos(self):
        return [(p.get('typeName',None), p.get('isPrimary',False), p.get('url', None)) for p in self.extra_data.get('photos', [])]

    def profile_pic(self):
        try:
            avatar = [url for type_of,primary,url in self.photos() if primary is True][0]
        except IndexError:
            avatar = settings.DEFAULT_MUGSHOT_URL

        return '<img src="%s" border="0"/>' % avatar
    profile_pic.allow_tags = True

    def contact_info(self):
        return self.extra_data.get('contactInfo', {})

    @property
    def full_name(self):
        return self.contact_info().get('fullName', None)

    @property
    def social_profile_names(self):
        return ', '.join([p.get('typeName', 'Unknown') for p in self.extra_data.get('socialProfiles', [])])

class GraphConnection(models.Model):
    """ Generic Database Model to store various provider abstractions """
    PROVIDERS = get_namedtuple_choices('PROVIDERS', (
        (0,'linkedin','Linkedin'),
        (1,'angel','Angel'),
      
    ))
    provider = models.IntegerField(choices=PROVIDERS.get_choices(), db_index=True)
    full_name = models.CharField(max_length=128)
    extra_data = JSONField(blank=True, null=True)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.full_name

"""
These classes are abstractions to allow massage
the remote apis data into a structure we can use
to populate the GraphConnection model
"""


class LawpalBaseConnection(object):
    """ 
    Generic Connection Provider 
    Provides an means of associating standardised
    graph object with a user
    """
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

    def associate(self, user):
        """ Create or associate this object with the specified user """
        logger.info('Associating %s with %s (%s:%s)' % (user.get_full_name(), self.full_name, self.provider, self.uid) )
        # get the integer val for the type
        provider_id = GraphConnection.PROVIDERS.get_value_by_name(self.provider)

        # get or create the graph object
        graph_obj, is_new = GraphConnection.objects.get_or_create(full_name=self.full_name, provider=provider_id)
        # update json_data
        graph_obj.extra_data = self.extra_data
        graph_obj.save()
        # associate our user with it
        graph_obj.users.add(user)

        logger.info('Graph Connection %s is_new: %s' % (self.full_name, is_new) )

        return graph_obj, is_new


class LinkedinConnection(LawpalBaseConnection):
    """ Linkedin Connection Provider """
    provider = 'linkedin'
    def get_full_name_from_data(self):
        return u'%s %s' % (self.extra_data.get('firstName'), self.extra_data.get('lastName'),)


class AngelConnection(LawpalBaseConnection):
    """ AngelList Connection Provider """
    provider = 'angel'
    def get_full_name_from_data(self):
        return u'%s' % self.extra_data.get('name')


class FullContactConnection(LawpalBaseConnection):
    """ FullContact Connection Provider """
    provider = 'fullcontact'
    def get_full_name_from_data(self):
        contact_info = self.extra_data.get('contactInfo')
        return u'%s' % contact_info.get('fullName')

