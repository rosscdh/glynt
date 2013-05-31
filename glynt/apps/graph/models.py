# -*- coding: utf-8 -*-
"""
Not Just standard django models
"""
import sys
from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

from jsonfield import JSONField
from glynt.apps.utils import get_namedtuple_choices

import logging
logger = logging.getLogger('lawpal.graph')

class FullContactData(models.Model):
    """ Provides a data source for a users fullcontact.com info """
    user = models.ForeignKey(User)
    extra_data = JSONField(blank=True, default={})

    @property
    def primary_photo_url(self):
        photos = self.photos()
        try:
            primary_photo = [url for type_of,primary,url in photos if primary is True][0]
        except IndexError:
            if len(photos) > 0:
                primary_photo = photos[0][2] # return the photo of the first record
            else:
                primary_photo = settings.DEFAULT_MUGSHOT_URL
        return primary_photo

    @property
    def full_name(self):
        return self.contact_info().get('fullName', None)

    @property
    def social_profile_names(self):
        return ', '.join([p.get('typeName', 'Unknown') for p in self.extra_data.get('socialProfiles', [])])

    @property
    def primary_profile(self):
        """ @BUSINESS_RULE: Set the profile to be any profile that has a 'bio' field
        if we have no isPrimary then set it to the profile that we do have a bio for """
        profiles = self.profiles()
        found_profile = {}

        for p in profiles:
            # set profile if we find a isPrimary
            if p.get('isPrimary', False) is True:
                found_profile = p
                break
            # set profile to any profile that has a bio if we dont already have a profile
            if found_profile == {} and p.get('bio', None) is not None:
                found_profile = p

        if found_profile == {}:
            # None Found so set it to the first
            try:
                found_profile = profiles[0]
            except IndexError:
                pass
        return found_profile

    def profiles(self):
        return self.extra_data.get('socialProfiles', [])

    def photos(self):
        return [(p.get('typeName',None), p.get('isPrimary',False), p.get('url', None)) for p in self.extra_data.get('photos', [])]

    def profile_pic(self):
        return '<img src="%s" border="0"/>' % self.primary_photo_url
    profile_pic.allow_tags = True

    def contact_info(self):
        return self.extra_data.get('contactInfo', {})

class GraphConnection(models.Model):
    """ Generic Database Model to store various provider abstractions """
    PROVIDERS = get_namedtuple_choices('PROVIDERS', (
        (0,'linkedin','Linkedin'),
        (1,'angel','Angel'),
    ))
    user = models.OneToOneField(User, null=True, blank=True)
    provider = models.IntegerField(choices=PROVIDERS.get_choices(), db_index=True)
    provider_uid = models.CharField(max_length=128, db_index=True)
    full_name = models.CharField(max_length=128)
    extra_data = JSONField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='connected_users')

    class Meta:
        unique_together = (('provider', 'provider_uid', 'full_name'),)

    def __unicode__(self):
        return self.full_name


# These classes are abstractions to allow massage of
# the remote apis data into a structure we can use
# to populate the GraphConnection model

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
        raise NotImplemented()

    def __str__(self):
        return '%s' % self.__unicode__().encode(sys.stdout.encoding)

    def __unicode__(self):
        return self.full_name

    def associate(self, user):
        """ Create or associate this object with the specified user """
        logger.info('Associating %s with %s (%s:%s)' % (user.get_full_name(), self.full_name, self.provider, self.uid))
        # get the integer val for the type
        provider_id = GraphConnection.PROVIDERS.get_value_by_name(self.provider)

        # get or create the graph object
        graph_obj, is_new = GraphConnection.objects.get_or_create(provider_uid=self.uid, provider=provider_id)

        # TODO: find existing user with uid and add as graph_obj.to_user
        try:
            to_user = User.objects.get(social_auth__uid=self.uid, social_auth__provider=self.provider)
            graph_obj.to_user = to_user
        except User.DoesNotExist:
            to_user = None

        # update json_data
        graph_obj.extra_data = self.extra_data
        graph_obj.save()
        # associate our user with it
        graph_obj.users.add(user)

        logger.info('%s Graph Connection %s is_new: %s' % (self.provider, self.full_name, is_new))

        return graph_obj, is_new


class LinkedinConnection(LawpalBaseConnection):
    """ Linkedin Connection, Provides
    access to the linkedin object model """
    provider = 'linkedin'

    def get_full_name_from_data(self):
        return u'%s %s' % (self.extra_data.get('firstName'), self.extra_data.get('lastName'),)


class AngelConnection(LawpalBaseConnection):
    """ AngelList Connection, Provides
    access to the linkedin object model """
    provider = 'angel'

    def get_full_name_from_data(self):
        return u'%s' % self.extra_data.get('name')


class FullContactConnection(LawpalBaseConnection):
    """ FullContact Connection, Provides
    access to the linkedin object model """
    provider = 'fullcontact'

    def get_full_name_from_data(self):
        contact_info = self.extra_data.get('contactInfo')
        return u'%s' % contact_info.get('fullName')
