# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.views.generic.base import View, TemplateView
from django.utils import simplejson as json
from django.db.utils import IntegrityError, DatabaseError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from glynt.apps.document.models import Document, ClientCreatedDocument
from glynt.apps.document.forms import ClientCreatedDocumentForm

from glynt.apps.document.views.document import DocumentView
from glynt.apps.document.views.utils import user_can_view_document, userdoc_from_request, FORM_GROUPS
from glynt.pybars_plus import PybarsPlus

import markdown
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import random

import logging
logger = logging.getLogger(__name__)


class MyDocumentView(DocumentView):
  """ Used when viewing a users own documents """
  def get_context_data(self, **kwargs):
    # call the parent dirctly and skip what the parent would do
    context = super(DocumentView, self).get_context_data(**kwargs)

    document_slug = slugify(self.kwargs['slug'])

    self.user_document = get_object_or_404(ClientCreatedDocument.objects.select_related(), slug=document_slug, owner=self.request.user)
    context['userdoc'] = self.user_document

    context['userdoc_form'] = ClientCreatedDocumentForm(instance=context['userdoc'])

    # Setup the document based on teh source_document of the viewed doc
    self.document = self.user_document.source_document
    context['object'] = self.document
    context['document'] = self.document.body
    context['default_data'] = json.dumps(self.user_document.data)
    context['invitee_list'] = json.dumps([{'id': i.pk, 'name': i.meta_data['to_name'], 'email': i.meta_data['to_email'], 'is_signed': i.is_signed} for i in self.user_document.documentsignature_set.all()])

    try:
      context['form_set'] = self.document.flyform.flyformset()
    except KeyError:
      context['form_set'] = FORM_GROUPS['no_steps']

    context['final_step_index'] = len(context['form_set']) + 1

    user_can_view_document(self.user_document, self.request.user)

    return context

# TODO this view represents both the create and the form validate (edit) views
# need to seperate them into two views
class ClientCreatedDocumentValidateFormView(View):
  """ A View to Simply Validate the current form and return errors if any
  Does not actually save data, saving data is done via the cookie """
  def post(self, request, *args, **kwargs):
    userdoc_pk = request.POST.get('id', None)
    userdoc_name = request.POST.get('name', None)

    form = ClientCreatedDocumentForm(request.POST)

    if not form.is_valid():
      return HttpResponse('[{"status":"%s", "message":"%s"}]' % (progress.pk, 'error', unicode(_('The form was not valid; please check your data "%s"' %(form.errors,) ))), status=400, content_type="application/json")
    else:
      if not request.user.is_authenticated():
        redirect_url = '%s?next=%s' % (settings.LOGIN_URL, reverse('document:view', kwargs={'slug':document_slug}))
        return HttpResponse('[{"userdoc_id": null, "url": "%s", "status":"%s", "message":"%s"}]' % (redirect_url, 'login_required', unicode(_('Login Required'))), status=200, content_type="application/json")

      document_slug = slugify(self.kwargs['slug'])
      document = get_object_or_404(Document, slug=document_slug)
      userdoc_pk = form.cleaned_data['id']

      client_document, is_new = userdoc_from_request(request.user, document, userdoc_pk)

      client_document.name = form.cleaned_data['name']

      saved = False
      counter = 1
      while saved is not True and counter < 15:
        # try to create a new documetn with updated name
        name = client_document.name
        if counter > 1:
          name = '%s %s' % (name, counter,)
        slug = slugify(name)

        try:
          ClientCreatedDocument.objects.exclude(pk=userdoc_pk).get(owner=request.user, slug=slug, name=name)
          counter = counter + 1
          saved = False
        except ClientCreatedDocument.DoesNotExist:
          client_document.name = name
          client_document.slug = slug
          client_document.save()
          saved = True

      redirect_url = client_document.get_absolute_url()

      return HttpResponse('[{"userdoc_id": %d, "url": "%s", "status":"%s", "message":"%s"}]' % (client_document.pk, redirect_url, 'success', unicode(_('Document Saved'))), status=200, content_type="application/json")


class PersistClientCreatedDocumentProgressView(View):
  """ Persist a clients cookie data as they progress through form """
  def post(self, request, *args, **kwargs):
    userdoc_current_progress = request.POST.get('current_progress', None)
    userdoc_pk = int(self.kwargs['pk'])

    # is never new
    progress, is_new = userdoc_from_request(user=request.user, source_doc=None, pk=userdoc_pk)

    if userdoc_current_progress:
      progress.data = userdoc_current_progress
      progress.save()

    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (progress.pk, 'success_persisted', unicode(_('Progress Persisted'))), status=200, content_type="application/json")


# @TODO rename to ClientCreatedDocumentExportView
class DocumentExportView(View):
    def post(self, request, *args, **kwargs):
      return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
      document_slug = slugify(self.kwargs['slug'])
      document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document','source_document__flyform'), slug=document_slug, owner=request.user)

      # @TODO Move all of this into a model method on ClientCreatedDocument
      data = []
      if type(document.source_document.flyform.defaults) is dict:
        data = document.source_document.flyform.defaults.items()
      if type(document.data) is dict:
        data = data + document.data.items()
      data = dict(data)
      if 'document_title' in data:
        data['document_title'] = document.name
      else:
        data['document_title'] = ''

      pybars_plus = PybarsPlus(document.body)
      body = pybars_plus.render(data)
      handlebars_template_body = mark_safe(markdown.markdown(body))

      html = render_to_string('document/export/base.html', {
        'body': handlebars_template_body
      })

      filename = '%s.pdf' % (document_slug,)
      pdf = StringIO.StringIO()
      result = pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")), pdf)

      if result.err:
        response = HttpResponse('[{"message":"%s"}]'%(pdf.err), status=401, content_type="text/json")
      else:
        response = HttpResponse(pdf.getvalue(), status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
        return response

      return response


class CloneClientCreatedDocumentView(View):
  """ Clone a specified document
  Structured strangely due to postgres not accepting catches by integrity error or databaseerror
  """
  def post(self, request, *args, **kwargs):
    client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
    client_document.pk = None # set the pk to null which will cause the ORM to save as a new object
    saved = False
    counter = 1
    while saved is not True and counter < 15:
      # try to create a new documetn with updated name
      name = 'Copy of %s' % (client_document.name,)
      if counter > 1:
        name = '%s %s' % (name, counter,)
      slug = slugify(name)

      try:
        ClientCreatedDocument.objects.get(owner=request.user, slug=slug, name=name)
        counter = counter + 1
        saved = False
      except ClientCreatedDocument.DoesNotExist:
        client_document.name = name
        client_document.slug = slug
        client_document.save()
        saved = True


    url = reverse('document:my_view', kwargs={'slug':client_document.slug})
    message = _("Cloned %s") % (client_document.name,)

    return HttpResponse('[{"userdoc_id": %d, "url":"%s", "status":"%s", "message":"%s"}]' % (client_document.pk, url, 'cloned', unicode(message),), status=200, content_type="application/json")


class DeleteClientCreatedDocumentView(View):
  def post(self, request, *args, **kwargs):
    client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
    client_document.is_deleted = True
    client_document.slug = '%d-%s' % (client_document.pk, client_document.slug[0:45],)
    client_document.save()
    message = _("Deleted %s, <a id='undelete-%d' class='undelete-my-document' href='%s'>undo</a>") % (client_document.name, client_document.pk, reverse('document:my_undelete', kwargs={'pk':client_document.pk}),)

    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', unicode(message),), status=200, content_type="application/json")


class UndoDeleteClientCreatedDocumentView(View):
  def post(self, request, *args, **kwargs):
    client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
    if client_document.is_deleted is True:
      client_document.is_deleted = False

      slug = base_slug = client_document.slug.replace('%d-'%(client_document.pk,), '')
      saved = False
      count = 1
      while saved is not True:
        try:
          client_document.slug = slug
          client_document.save()
          saved = True
        except IntegrityError:
          slug = '%s-%d' %(base_slug, count,)
          count = count+1
          saved = False
    message = _("Reactivated '%s'") % (client_document.name,)
    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', message,), status=200, content_type="application/json")

