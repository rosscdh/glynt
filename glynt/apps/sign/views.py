# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.views.generic import UpdateView
from django.views.generic.edit import BaseFormView

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.forms import DocumentSignatureForm

from glynt.apps.sign.utils import encode_data, decode_data


class DocumentSignatureInviteToSignView(BaseFormView):
  """ Process the invitation submission"""
  http_method_names = ['post', 'delete']

  def post(self, request, *args, **kwargs):
    # Create new model based on list passed in
    doc = get_object_or_404(ClientCreatedDocument, pk=kwargs['pk'])
    print request.POST
    key_hash, hash_data = encode_data([doc.pk, doc.name])
    form = DocumentSignatureForm(initial={'document': doc, 'key_hash': key_hash})
    return HttpResponse('[{"key_hash":%s, "hash_data": %s}]' % (key_hash, hash_data), status=200)
    # if form.is_valid():
    #   return self.form_valid(form)
    # else:
    #   return self.form_invalid(form)


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