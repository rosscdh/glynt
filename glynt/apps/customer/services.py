# -*- coding: UTF-8 -*-
import os

from django.contrib.auth.models import User

from glynt.apps.default.mixins import ChangeUserDetailsMixin

try:
    from glynt.apps.customer.models import Customer, _customer_upload_photo
except ImportError:
    # Customer appears to already be in sys.modules
    pass

import logging
logger = logging.getLogger('lawpal.services')


class EnsureCustomerService(ChangeUserDetailsMixin):
    """ Set up a startup customer """
    customer = None

    def __init__(self, user, **kwargs):
        self.user = user
        self.summary = kwargs.pop('summary', None)
        self.bio = kwargs.pop('bio', None)
        self.photo = kwargs.pop('photo', None)
        self.data = kwargs

    def update_user_profile(self):
        # update the is_customer attribute
        profile = self.user.profile
        profile.profile_data['is_customer'] = True
        profile.save(update_fields=['profile_data'])

    def save_photo(self, photo):
        if photo and self.customer.photo != photo:  # only if its not the same image
            logger.info('New photo for %s' % self.customer)
            photo_file = os.path.basename(self.photo.file.name)  # get base name
            # try:
            # move from ajax_uploads to the model desired path
            new_path = _customer_upload_photo(instance=self.customer, filename=photo_file)
            photo.file.storage.save(new_path, photo.file)  # save to new path
            # will now upload to s3
            self.customer.photo.save(name=photo_file, content=photo.file)
            self.customer.user.profile.mugshot.save(name=photo_file, content=photo.file)
            logger.info('Saved new photo %s for %s' % (photo.file, self.customer))
            # except Exception as e:
            #     logger.error('Could not save user photo %s for %s: %s' % (photo.file, self.customer, e))

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
