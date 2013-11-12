# -*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
import json

from models import Lawyer
from glynt.apps.firm.services import EnsureFirmService
from tasks import send_profile_setup_email

import logging
logger = logging.getLogger('lawpal.services')


class EnsureLawyerService(object):
    """ Setup a Lawyer and his related Firm and Office """
    lawyer = None
    firm = None
    default_volume_matrix = unicode('[0]')
    default_volume_matrix_by_year = unicode('{"2010":0,"2011":0,"2012":0,"2013":0}')

    def __init__(self, user, firm_name=None, offices=[], **kwargs):
        self.user = user
        self.firm_name = firm_name
        self.offices = offices

        self.form = kwargs.pop('form', None)
        self.role = kwargs.pop('role', None)

        # remove unwanted fields
        kwargs.pop('bar_membership_input', None)
        kwargs.pop('websites_input', None)

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
        if fields_to_update:
            User.objects.filter(pk=self.user.pk).update(**dict(fields_to_update))

        # Update the password if present in the form
        # being present in the form means that this is a new user
        if self.form is not None and self.form.cleaned_data.get('password', None) is not None:
            self.user.set_password(self.form.cleaned_data.get('password', None))
            self.user.save()
            # Send the email on profile setup
            self.send_congratulations_email(user=self.user)

    def update_user_profile(self):
        # update the is_lawyer attribute
        profile = self.user.profile
        profile.profile_data['is_lawyer'] = True
        profile.save(update_fields=['profile_data'])

    def process(self):
        self.update_user()
        self.update_user_profile()
        self.lawyer, self.lawyer_is_new = Lawyer.objects.get_or_create(user=self.user)

        # user may already be associated with a firm
        firms = self.lawyer.firm_lawyers.all()
        if firms:
            self.firm = firms[0]
            logger.info('Firm %s is associated with lawyer %s ' % (self.lawyer.user.username, self.firm.name))

        if self.form is not None:
            self.perform_update()

    def save_photo(self, photo):
        if photo and self.lawyer.photo != photo: # only if its not the same image
            logger.info('New photo for %s' % self.lawyer)
            photo_file = os.path.basename(photo.file.path)# get base name
            try:
                self.lawyer.photo.save(photo_file, photo.file)
                self.lawyer.user.profile.mugshot.save(photo_file, photo.file)
                logger.info('Saved new photo %s for %s' % (photo.file, self.lawyer))
            except Exception as e:
                logger.error('Could not save user photo %s for %s: %s' % (photo.file, self.lawyer, e))


    def send_congratulations_email(self, user):
        # Send profile email
        send_profile_setup_email(user=user)

    def volume_matrix(self, lawyer_data):
        # Updates to the JSON Data object for the Lawyer
        volume_types = (('companies_advised', unicode('[0]')), ('volume_incorp_setup', self.default_volume_matrix), \
                        ('volume_seed_financing', self.default_volume_matrix), ('volume_series_a', self.default_volume_matrix), \
                        ('volume_ip', self.default_volume_matrix), ('volume_other', self.default_volume_matrix), \
                        ('volume_by_year', self.default_volume_matrix_by_year),)

        for vt, default in volume_types:
            try:
                # get value from sent data
                val = self.data.get(vt, default)
            except ValueError:
                # errored out
                val = default
            try:
                val = json.loads(val)
            except ValueError:
                val = [0]
            lawyer_data[vt] = val

        return lawyer_data

    def perform_update(self):
        """
        DANGER: we make use of json fields to store flexible extended data
        We also use the .update() methods for quick and easy updates that are less
        load inducing. Beware you cannot do an .update() on the Lawyer.data field.
        It must go via the .save() method or things get incorrectly encoded
        """
        fields_to_update = {}

        if self.role:
            self.lawyer.role = self.role

        if self.data:
            self.data['bar_membership'] = json.loads(self.data.get('bar_membership', '[]')) if self.data.get('bar_membership', '[]') != '' else []
            self.data['websites'] = json.loads(self.data.get('websites', '[]')) if self.data.get('websites', '[]') != '' else []
            self.lawyer.data = self.data

        if self.data.get('photo', None) is not None:
            # pop so it does not get serialized
            self.save_photo(self.data.pop('photo'))

        # Update standard model fields
        fields_to_update.update(summary = self.data.get('summary', None))
        fields_to_update.update(bio = self.data.get('bio', None))
        # remove empty items
        fields_to_update = [(k,v) for k,v in fields_to_update.items() if v is not None]

        # perform volume matrix update
        lawyer_data = self.volume_matrix(lawyer_data=self.lawyer.data)

        # add the JSON object and perform lawyer save on that field only
        self.lawyer.data = lawyer_data
        self.lawyer.save()

        # Primary lawyer update query
        # Will always be present due to the previous get_or_create
        Lawyer.objects.filter(pk=self.lawyer.pk).update(**dict(fields_to_update))

        logger.info('get_or_create:lawyer %s is_new: %s' % (self.lawyer.user.username, self.lawyer_is_new,))

        if self.firm_name is None:
            logger.info('Firm name not provided for lawyer %s ' % (self.lawyer.user.username,))
        else:
            logger.info('Firm name "%s" was provided for lawyer %s ' % (self.firm_name, self.lawyer.user.username,))
            self.data.update({
                'user': self.user,
                'lawyer': self.lawyer
            })
            firm_service = EnsureFirmService(firm_name=self.firm_name, offices=self.offices, **self.data)
            firm_service.process()
            self.firm = firm_service.firm

