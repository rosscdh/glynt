# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from glynt.apps.sign.models import DocumentSignature


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