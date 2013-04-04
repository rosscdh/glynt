# -*- coding: utf-8 -*-
import os
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

        self.role = kwargs.pop('position', None)
        self.data = kwargs

    # def role_id(self, position):
    #     """ Return the role_id that matches the user input Role """
    #     if position is not None:
    #         position = position.lower().strip()
    #         role_id = next((role_id for role_id,role in Lawyer.LAWYER_ROLES.get_choices() if role.lower() == position), [Lawyer.LAWYER_ROLES.unknown])
    #     else:
    #         role_id = Lawyer.LAWYER_ROLES.unknown
    #     return role_id

    def update_user(self):
        self.title = self.data.get('title', None)

        self.first_name = self.data.get('first_name', None)
        self.last_name = self.data.get('last_name', None)
        self.email = self.data.get('email', None)

        if self.first_name is not None:
            self.user.first_name = self.first_name

        if self.last_name is not None:
            self.user.last_name = self.last_name

        if self.email is not None:
            self.user.email = self.email

        self.user.save()

    def process(self):
        self.update_user()

        self.lawyer, lawyer_is_new = Lawyer.objects.get_or_create(user=self.user)

        if self.role:
            self.lawyer.role = self.role

        if self.data:
            self.lawyer.data = self.data

        if self.data.get('photo', None) is not None:
            photo = self.data.pop('photo') # remove so it does not get serialized

            if self.lawyer.photo != photo: # only if its not the same image
                photo_file = os.path.basename(photo.file.path)# get base name
                self.lawyer.photo.save(photo_file, photo.file)


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

        logger.info('get_or_create:lawyer %s is_new: %s' % (self.lawyer.user.username, lawyer_is_new,))

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
                logger.info('Firm %s is assocaited with lawyer %s ' % (self.lawyer.user.username, self.firm.name))
            
