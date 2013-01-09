# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap.forms import BootstrapModelForm, Fieldset

from glynt.apps.document.models import Document
from glynt.apps.document.models import ClientCreatedDocument


class DocumentForm(BootstrapModelForm):
  class Meta:
    model = Document
    layout = (
        Fieldset('Document Authoring', 'body'),
        Fieldset('Document Properties', 'name', 'slug', 'owner', 'summary', 'doc_status', 'is_public', 'doc_cats', 'tags'),
    )


class ClientDocumentForm(forms.ModelForm):
  class Meta:
    model = ClientCreatedDocument