# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from glynt.apps.sign.models import DocumentSignature

import logging
logger = logging.getLogger('django.request')


class DocumentSignatureForm(forms.ModelForm):
  class Meta:
    model = DocumentSignature

  def clean_key_hash(self):
    """ dont allow hashes tobe used more than once, and dont (yet) rely on db exceptions"""
    key_hash = self.cleaned_data.get('key_hash')
    try:
        DocumentSignature.objects.get(key_hash=key_hash)
    except DocumentSignature.DoesNotExist:
        return key_hash
    else:
        raise forms.ValidationError(_('This hash %s has already been issued'%(key_hash,)))

  def clean_user(self):
      """ @TODO turn the user createion aspect into a service """
      meta_data = self.data['meta_data'].copy()
      is_new = False
      to_email = meta_data.get('to_email', None)
      to_name = meta_data.get('to_name', None)

      if to_email is not None:
          # Create the user or associate an existing one with this 
          try:
              user = User.objects.filter(email=to_email)[0]
          except User.DoesNotExist:
              user = User.objects.create(email=to_email)
              is_new = True

          if is_new == True:
              username = None
              first_name = None
              last_name = None

              # we have a to_email
              username = slugify(to_email)
              name = to_name.split(' ')
              try:
                  first_name = name[0]
                  last_name = ' '.join(name[1:])
              except:
                  first_name = to_name

              logger.info('Creating user: %s %s %s'%(first_name, last_name, user.email,))

              user.first_name = first_name
              user.last_name = last_name
              user.username = username
              user.save()

          logger.info('Bound %s user is_new:%s to Signature'%(user.email, is_new,))
          return user