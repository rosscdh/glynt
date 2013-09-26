# -*- coding: UTF-8 -*-
""" 
"""
from bunch import Bunch

from django.core.exceptions import ValidationError

import logging
logger = logging.getLogger('lawpal.services')


class BaseUserBunch(Bunch):
    user = None
    data = None
    data_bag_key = None

    def __init__(self, user=None):
        if not user:
            raise ValidationError('user must be defined')
        self.user = user

    def get_data_bag(self):
        try:
            profile_data = self.user.profile.profile_data[self.data_bag_key]
        except KeyError:
            logger.info('profile_data key "%s" does not exist returning dict' % (self.data_bag_key,))
            profile_data = {}
        return profile_data

    def save(self, **kwargs):
        profile = self.user.profile
        profile_data = profile.profile_data

        profile_data[self.data_bag_key] = kwargs
        profile.profile_data = profile_data

        return profile.save(update_fields=['profile_data'])


class UserCompanyBunch(BaseUserBunch):
    data_bag_key = 'company'


class UserCompanyOfficersBunch(BaseUserBunch):
    data_bag_key = 'company.officers'
