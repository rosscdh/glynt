# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.utils import simplejson as json
from models import Lawyer
from glynt.apps.firm.services import EnsureFirmService

import logging
logger = logging.getLogger('lawpal.services')
import pdb

class EnsureLawyerService(object):
    """ Setup a Lawyer and his related Firm and Office """
    lawyer = None
    firm = None
    default_volume_matrix = '{"2010":0,"2011":0,"2012":0}'
    def __init__(self, user, firm_name=None, offices=[], **kwargs):
        self.user = user
        self.firm_name = firm_name
        self.offices = offices

        self.form = kwargs.pop('form', None)
        self.role = kwargs.pop('position', None)
        self.data = kwargs

    def update_user(self):
        fields_to_update = {}
        fields_to_update.update(first_name = self.data.get('first_name', None))
        fields_to_update.update(last_name = self.data.get('last_name', None))
        fields_to_update.update(email = self.data.get('email', None))
        # remove empty items
        fields_to_update = [(k,v) for k,v in fields_to_update.items() if v is not None]
        # update the user only if changes happened
        # this avoides superflous saves, and also uses update and not the heavy save method
        User.objects.filter(pk=self.user.pk).update(**dict(fields_to_update))

    def process(self):
        self.update_user()
        self.lawyer, self.lawyer_is_new = Lawyer.objects.get_or_create(user=self.user)

        # usermay already be associated with a firm
        firms = self.user.firm_lawyers.all()
        if firms:
            self.firm = firms[0]
            logger.info('Firm %s is associated with lawyer %s ' % (self.lawyer.user.username, self.firm.name))

        if self.form is not None:
            self.perform_update()

    def save_photo(self, photo):
        if photo and self.lawyer.photo != photo: # only if its not the same image
            logger.info('New photo for %s' % self.lawyer)
            photo_file = os.path.basename(photo.file.path)# get base name
            self.lawyer.photo.save(photo_file, photo.file)
            self.lawyer.user.profile.mugshot.save(photo_file, photo.file)
            logger.info('Saved new photo %s for %s' % (photo.file, self.lawyer))

    def perform_update(self):
        fields_to_update = {}

        if self.role:
            self.lawyer.role = self.role

        if self.data:
            self.lawyer.data = self.data

        if self.data.get('photo', None) is not None:
            # pop so it does not get serialized
            self.save_photo(self.data.pop('photo'))

        # Update standard model fields
        fields_to_update.update(summary = self.data.get('summary', None))
        fields_to_update.update(bio = self.data.get('bio', None))
        # remove empty items
        fields_to_update = [(k,v) for k,v in fields_to_update.items() if v is not None]

        # Updates to the JSON Data object for the Lawyer
        tmp_data = {}
        data = self.lawyer.data

        tmp_data.update(startups_advised = self.data.get('startups_advised', '[]'))

        tmp_data.update(volume_incorp_setup = self.data.get('volume_incorp_setup', self.default_volume_matrix))
        tmp_data.update(volume_seed_financing = self.data.get('volume_seed_financing', self.default_volume_matrix))
        tmp_data.update(volume_series_a = self.data.get('volume_series_a', self.default_volume_matrix))
        # remove empty items
        tmp_data = [(k,v) for k,v in tmp_data.items() if v is not None]

        # add the JSON object and perform lawyer save on that field only
        if tmp_data:
            self.lawyer.data.update(tmp_data)
            self.lawyer.save()
            logger.info('lawyer:fields:data update %s' % self.lawyer.user.username)

        # Primary lawyer update query
        # Will always be present due to the previous get_or_create
        Lawyer.objects.filter(pk=self.lawyer.pk).update(**dict(fields_to_update))

        logger.info('get_or_create:lawyer %s is_new: %s' % (self.lawyer.user.username, self.lawyer_is_new,))

        if self.firm_name is None:
            logger.info('Firm name not provided for lawyer %s ' % (self.lawyer.user.username,))
        else:
            logger.info('Firm name "%s" was provided for lawyer %s ' % (self.firm_name, self.lawyer.user.username,))
            self.data.update({
                'create_office': False, # May not create office, as the csv for Lawyers does not contain the right info.. use import_firms
                'user': self.user,
                'lawyer': self.lawyer
            })
            firm_service = EnsureFirmService(firm_name=self.firm_name, offices=self.offices, **self.data)
            firm_service.process()
            self.firm = firm_service.firm
