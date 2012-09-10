# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from django.views.generic import UpdateView

from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.forms import DocumentSignatureForm


class DocumentSignatureView(UpdateView):
  """
  View to allow an invited signatory to sign a document
  """
  form_class = DocumentSignatureForm
  model = DocumentSignature
  template_name = 'sign/sign_document.html'

  def get_success_url(self):
    url = reverse('sign:complete', kwargs={'pk': self.object.document.pk})
    return url

  def get_object(self, queryset=None):
    """ return the signature by related document pk and the invited signatory user """
    pk = self.kwargs.get(self.pk_url_kwarg, None)
    if pk is not None:
        ob = get_object_or_404(self.model, document=pk, key_hash=self.kwargs['hash'])
        return ob
    else:
        raise AttributeError(u"You must specify a document pk for this view")