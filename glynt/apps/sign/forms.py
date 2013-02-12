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

      to_email = meta_data.get('to_email', None)
      to_name = meta_data.get('to_name', None)
      username = None
      first_name = None
      last_name = None

      if to_email is not None:
          # we have a to_email
          username = slugify(to_email)
          name = to_name.split(' ')
          try:
              first_name = name[0]
              last_name = ' '.join(name[1:])
          except:
              first_name = to_name

          logger.info('%s %s'%(first_name, last_name,))

          # Create the user or associate an existing one with this 
          user, is_new = User.objects.get_or_create(email=to_email, first_name=first_name, last_name=last_name)
          if is_new == True:
              user.username = username
              user.save()

          logger.info('Bound %s user is_new:%s to Signature'%(user.email, is_new,))
          return user