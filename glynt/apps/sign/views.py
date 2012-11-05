# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView
from django.views.generic.edit import BaseFormView, ProcessFormView, FormMixin
from django.views.generic.detail import BaseDetailView


from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.sign.models import DocumentSignature
from glynt.apps.sign.forms import DocumentSignatureForm

from glynt.apps.sign.utils import encode_data

import datetime
from django.utils.timezone import utc


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
    invitee_created_list = []

    for email, name in invitees:
      key_hash, hash_data = encode_data([doc.pk, email])
      meta_data = {
        'to_name': name,
        'to_email': email,
        'invited_by_pk': request.user.pk,
        'invited_by_name': request.user.get_full_name() if request.user.get_full_name() else request.user.username,
        'invited_by_email': request.user.email
      }
      form = DocumentSignatureForm({'document': doc.pk, 'key_hash': key_hash, 'hash_data': hash_data, 'meta_data': meta_data})
      if form.is_valid():
        invitee = form.save()
        invitee_created_list.append({"pk": invitee.pk, "email": invitee.meta_data['to_email'], "name": invitee.meta_data['to_name'], "key_hash": key_hash})

    return HttpResponse('%s' % (json.dumps(invitee_created_list)), status=200)


class DeleteInviteToSignView(BaseFormView):
  http_method_names = ['delete']

  def delete(self, request, *args, **kwargs):
    """ Delete the specified signature object """
    pk = kwargs['invitation_pk']
    document_signature = get_object_or_404(DocumentSignature, pk=pk, document__owner=request.user)

    try:
      document_signature.delete()
      return HttpResponse('%s' % json.dumps({'id': pk, 'deleted': True}), status=200)
    except:
      return HttpResponse('%s' % json.dumps({'id': pk, 'deleted': False}), status=501)


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


class ProcessSignDocumentView(UpdateView):
  """ View to accept the invitees signature and congratulate them on success """
  http_method_names = ['post']
  model = DocumentSignature
  form_class = DocumentSignatureForm

  def get_success_url(self):
    return reverse('sign:default', kwargs={'pk': self.object.document.pk, 'hash': self.object.key_hash})

  def get_object(self):
    return get_object_or_404(self.model.objects.select_related('document', 'document__source_document', 'document__source_document__flyform'), pk=self.kwargs['pk'], key_hash=self.kwargs['hash'])

  def form_valid(self, form=None):
    return HttpResponseRedirect(self.get_success_url())

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()

    form_class = self.get_form_class()
    form = self.get_form(form_class)

    if not self.object.is_signed:
      signature = request.POST.get('output', None)
      date_signed = datetime.datetime.utcnow().replace(tzinfo=utc)
      self.object.signature = signature
      self.object.is_signed = True
      self.object.date_signed = date_signed
      self.object.meta_data['signed_at'] = date_signed
      self.object.meta_data['signee_ip'] = request.META.get('REMOTE_ADDR')
      self.object.meta_data['signee_host'] = request.META.get('REMOTE_HOST')
      self.object.meta_data['signee_useragent'] = request.META.get('HTTP_USER_AGENT')
      self.object.meta_data['signee_referer'] = request.META.get('HTTP_REFERER') # should not have one? security check?

      self.object.save()
      messages.success(request, _('You have successfully signed this document'))

    return self.form_valid(form)


class RenderSignatureImageView(BaseDetailView):
  http_method_names = ['get']
  model = DocumentSignature

  def get_object(self):
    return get_object_or_404(self.model, document__pk=self.kwargs['pk'], key_hash=self.kwargs['hash'])

  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    response = HttpResponse(mimetype="image/png")

    image = self.object.signature_as_image()
    image.save(response, "PNG")
    return response