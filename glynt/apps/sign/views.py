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

# doc = ClientCreatedDocument.objects.get(pk=1)
# email = 'ross@weareml.com'
# key_hash, hash_data = encode_data([doc.pk, email])
# form = DocumentSignatureForm({'document': doc.pk, 'key_hash': key_hash, 'hash_data': hash_data})

class DocumentSignatureInviteToSignView(BaseFormView):
  """ Process the invitation submission"""
  http_method_names = ['post', 'delete']

  def post(self, request, *args, **kwargs):
    # Create new model based on list passed in
    doc = get_object_or_404(ClientCreatedDocument, pk=kwargs['pk'])

    names = request.POST.getlist('name')
    emails = request.POST.getlist('email')
    invitees = [(emails[index], name) for index, name in enumerate(names)]

    for email, name in invitees:
      key_hash, hash_data = encode_data([doc.pk, email])
      meta = {
        'to_name': name,
        'to_email': email,
        'invited_by': request.user.get_full_name() if request.user.get_full_name() else request.user.username
      }
      form = DocumentSignatureForm({'document': doc.pk, 'key_hash': key_hash, 'hash_data': hash_data, 'meta': meta})
      if form.is_valid():
        form.save()

    return HttpResponse('[{"key_hash":%s, "hash_data": %s}]' % (key_hash, hash_data), status=200)


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