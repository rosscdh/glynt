# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap.forms import BootstrapModelForm, Fieldset

from glynt.apps.document.models import Document


class DocumentForm(BootstrapModelForm):
    class Meta:
        model = Document
        exclude = ('slug',)
        layout = (
            Fieldset('Document Authoring', 'body'),
            Fieldset('Document Properties', 'name', 'owner', 'summary', 'doc_status', 'is_public', 'doc_cats', 'tags'),
        )