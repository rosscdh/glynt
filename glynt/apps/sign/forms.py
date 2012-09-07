# -*- coding: utf-8 -*-
from django import forms

from glynt.apps.sign.models import DocumentSignature



class DocumentSignatureForm(forms.ModelForm):
  class Meta:
    model = DocumentSignature
