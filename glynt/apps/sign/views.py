# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from django.views.generic import UpdateView
from django.views.generic.edit import BaseFormView, ProcessFormView
from django.views.generic.detail import BaseDetailView

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.forms import DocumentSignatureForm

from glynt.apps.sign.utils import encode_data, decode_data

from signpad2image.signpad2image import s2i

import datetime


class ProcessInviteToSignView(BaseFormView):
  """ Process the invitation submission
  The "view" that posts to this Process is a javascript widget
  and not a normal django view
  """
  http_method_names = ['post']

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


class SignDocumentView(UpdateView):
  """
  View to allow an invited signatory to sign and review a document
  """
  form_class = DocumentSignatureForm
  model = DocumentSignature
  template_name = 'sign/sign_document.html'

  def get_success_url(self):
    url = reverse('sign:invite_complete', kwargs={'pk': self.object.document.pk})
    return url

  def get_object(self, queryset=None):
    """ return the signature by related document pk and the invited signatory user """
    pk = self.kwargs.get(self.pk_url_kwarg, None)
    if pk is not None:
        ob = get_object_or_404(self.model.objects.select_related('document', 'document__source_document', 'document__source_document__flyform'), document=pk, key_hash=self.kwargs['hash'])
        return ob
    else:
        raise AttributeError(u"You must specify a document pk for this view")

  def get_context_data(self, **kwargs):
    context = super(SignDocumentView, self).get_context_data(**kwargs)
    context['userdoc'] = self.object.document
    context['document_data'] = self.object.document.data_as_json()

    return context

class ProcessSignDocumentView(ProcessFormView):
  """ View to accept the invitees signature and congratulate them on success """
  http_method_names = ['post']
  model = DocumentSignature

  def post(self, request, *args, **kwargs):
    document_signature = get_object_or_404(self.model.objects.select_related('document', 'document__source_document', 'document__source_document__flyform'), pk=self.kwargs['pk'], key_hash=self.kwargs['hash'])

    if not document_signature.is_signed:
      signature = request.POST.get('output',None)
      document_signature.signature = signature
      document_signature.is_signed = True
      document_signature.meta_data['signed_at'] = datetime.datetime.utcnow()
      document_signature.save()

    return redirect(reverse('sign:process_signature_complete', kwargs={'pk': document_signature.pk, 'hash': document_signature.key_hash}))

class RenderSignatureImageView(BaseDetailView):
  http_method_names = ['get']
  model = DocumentSignature

  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    response = HttpResponse(mimetype="image/png")
    try:
      #build the new image
      image = s2i(json.dumps(self.object.signature), input_image=settings.BLANK_SIG_IMAGE[0])
    except(self.object.DoesNotExist):
      #If it wasn't in the database, then return the nosig image
      image = s2i("", force_no_sig_image=True, nosig_image=settings.NO_SIG_IMAGE[0])
    #return the HttpResponse object to the client.
    image.save(response, "PNG")
    return response