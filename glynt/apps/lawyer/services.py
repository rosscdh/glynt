# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.utils import simplejson as json
from models import Lawyer
from glynt.apps.firm.services import EnsureFirmService

import logging
logger = logging.getLogger('lawpal.services')


class EnsureLawyerService(object):
    """ Setup a Lawyer and his related Firm and Office """
    lawyer = None
    firm = None
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
        User.objects.filter(pk=self.user.pk).update(**dict(fields_to_update))

    def process(self):
        self.update_user()
        self.lawyer, self.lawyer_is_new = Lawyer.objects.get_or_create(user=self.user)
        if self.form is not None:
            self.perform_update()

    def perform_update(self):
        if self.role:
            self.lawyer.role = self.role

        if self.data:
            self.lawyer.data = self.data

        if self.data.get('photo', None) is not None:
            photo = self.data.pop('photo') # remove so it does not get serialized

            if self.lawyer.photo != photo: # only if its not the same image
                logger.info('New photo for %s' % self.lawyer)
                photo_file = os.path.basename(photo.file.path)# get base name
                self.lawyer.photo.save(photo_file, photo.file)
                self.lawyer.user.profile.mugshot.save(photo_file, photo.file)


        if self.data.get('startups_advised', None) is not None:
            self.lawyer.data['startups_advised'] = json.loads(self.data.get('startups_advised'))

        if self.data.get('summary', None) is not None:
            self.lawyer.summary = self.data.get('summary')

        if self.data.get('bio', None) is not None:
            self.lawyer.bio = self.data.get('bio')

        if self.data.get('volume_incorp_setup', None) is not None:
            self.lawyer.data['volume_incorp_setup'] = json.loads(self.data.get('volume_incorp_setup'))

        if self.data.get('volume_seed_financing', None) is not None:
            self.lawyer.data['volume_seed_financing'] = json.loads(self.data.get('volume_seed_financing'))

        if self.data.get('volume_series_a', None) is not None:
            self.lawyer.data['volume_series_a'] = json.loads(self.data.get('volume_series_a'))

        self.lawyer.save()

        logger.info('get_or_create:lawyer %s is_new: %s' % (self.lawyer.user.username, self.lawyer_is_new,))

        if self.firm_name is not None:

            self.data.update({
                'create_office': False, # May not create office, as the csv for Lawyers does not contain the right info.. use import_firms
                'user': self.user,
                'lawyer': self.lawyer
            })

            firm_service = EnsureFirmService(firm_name=self.firm_name, offices=self.offices, **self.data)
            firm_service.process()
            self.firm = firm_service.firm

        else:

            logger.info('Firm name not provided for lawyer %s ' % (self.lawyer.user.username,))
            # usermay already be associated with a firm
            firms = self.user.firm_lawyers.all()
            if firms:
                self.firm = firms[0]
                logger.info('Firm %s is associated with lawyer %s ' % (self.lawyer.user.username, self.firm.name))
            
