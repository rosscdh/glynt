# -*- coding: UTF-8 -*-
import os

from django.contrib.auth.models import User

try:
    from glynt.apps.customer.models import Customer
except ImportError:
    # Customer appears to already be in sys.modules
    pass

import logging
logger = logging.getLogger('lawpal.services')


class EnsureCustomerService(object):
    """ Set up a startup customer """
    customer = None

    def __init__(self, user, **kwargs):
        self.user = user
        self.summary = kwargs.pop('summary', None)
        self.bio = kwargs.pop('bio', None)
        self.photo = kwargs.pop('photo', None)
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

    def update_user_profile(self):
        # update the is_customer attribute
        profile = self.user.profile
        profile.profile_data['is_customer'] = True
        profile.save(update_fields=['profile_data'])

    def save_photo(self, photo):
        if photo and self.customer.photo != photo:  # only if its not the same image
            logger.info('New photo for %s' % self.customer)
            photo_file = os.path.basename(self.photo.file.name)  # get base name
            try:
                self.customer.photo.save(photo_file, photo.file)
                self.customer.user.profile.mugshot.save(photo_file, photo.file)
                logger.info('Saved new photo %s for %s' % (photo.file, self.customer))
            except Exception as e:
                logger.error('Could not save user photo %s for %s: %s' % (photo.file, self.customer, e))

    def process(self):
        self.update_user()
        self.update_user_profile()
        self.customer, is_new = Customer.objects.get_or_create(user=self.user)
        logger.info("Processing customer %s (is_new: %s)" % (self.user.get_full_name(), is_new,))

        if self.summary:
            self.customer.summary = self.summary

        if self.bio:
            self.customer.bio = self.bio

        if self.data:
            self.customer.data.update(self.data)

        if self.photo:
            # pop so it does not get serialized
            self.save_photo(self.photo)

        logger.info("Saving customer %s", self.user)
        self.customer.save()
        return self.customer
