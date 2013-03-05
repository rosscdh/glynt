# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404

from django.views.generic.base import View
from django.views.generic import DetailView

from django.utils import simplejson as json
from django.db.utils import IntegrityError
from django.template import Context

from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument
from glynt.apps.document import tasks

from glynt.apps.document.views.document import DocumentView
from glynt.apps.document.views.utils import user_can_view_document, userdoc_from_request, FORM_GROUPS
from glynt.apps.sign.services import SignaturePageService

import logging
logger = logging.getLogger(__name__)


class DocumentQRCode(DetailView):
    model = ClientCreatedDocument

    def render_to_response(self, context, **response_kwargs):
        image_data = context['object'].qr_code_image()
        response = HttpResponse(mimetype="image/png")
        image_data.save(response, "PNG")
        return response



class MyDocumentView(DocumentView):
    """ Used when viewing a users own documents """
    def get_context_data(self, **kwargs):
    # call the parent dirctly and skip what the parent would do
    # the item being skipped here is the user_can_view_document
        context = super(DocumentView, self).get_context_data(**kwargs)

        self.user_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
        user_can_view_document(self.user_document, self.request.user)

        # Setup the document based on the source_document of the viewed doc
        self.document = self.user_document.source_document

        context['userdoc'] = self.user_document
        context['object'] = self.document
        context['document'] = self.user_document.documenthtml_set.all()[0]
        context['default_data'] = json.dumps(self.user_document.doc_data)

        return context


class ReviewClientCreatedView(MyDocumentView):
    """ Show an overview of the selected document """
    template_name = 'document/review.html'
    def get_context_data(self, **kwargs):
        context = super(ReviewClientCreatedView, self).get_context_data(**kwargs)

        signature_preview = SignaturePageService(document=self.user_document)

        context['document_html'] = self.user_document.documenthtml_set.all()[0].render()
        context['signature'] = signature_preview.render()
        context['next'] = reverse('document:my_review', kwargs={'pk': self.user_document.pk})
        return context


# TODO this view represents both the create and the form validate (edit) views
# need to seperate them into two views
class ValidateClientCreatedDocumentFormView(View):
    """ A View to Simply Validate the current form and return errors if any
    Does not actually save data, saving data is done via the cookie """
    def post(self, request, *args, **kwargs):
        userdoc_pk = request.POST.get('id', None)

        form = ClientCreatedDocumentForm(request.POST)

        if not form.is_valid():
            return HttpResponse('[{"status":"%s", "message":"%s"}]' % ('error', unicode(_('The form was not valid; please check your data "%s"' %(form.errors,) ))), status=400, content_type="application/json")
        else:
            if not request.user.is_authenticated():
                redirect_url = '%s?next=%s' % (settings.LOGIN_URL, reverse('document:view', kwargs={'pk': self.kwargs['pk']}))
                return HttpResponse('[{"userdoc_id": null, "url": "%s", "status":"%s", "message":"%s"}]' % (redirect_url, 'login_required', unicode(_('Login Required'))), status=200, content_type="application/json")

            document = get_object_or_404(Document, pk=self.kwargs['pk'])
            userdoc_pk = form.cleaned_data['id']

            client_document, is_new = userdoc_from_request(request.user, document, userdoc_pk)

            client_document.name = form.cleaned_data['name']

            client_document.name = name
            client_document.save()
            saved = True

            # Notification
            tasks.document_created(document=client_document)

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
            progress.doc_data = userdoc_current_progress
            progress.save()

        return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (progress.pk, 'success_persisted', unicode(_('Progress Persisted'))), status=200, content_type="application/json")


class CloneClientCreatedDocumentView(View):
    """ Clone a specified document
    Structured strangely due to postgres not accepting catches by integrity error or databaseerror
    """
    def post(self, request, *args, **kwargs):
        client_document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document'), pk=self.kwargs['pk'])
        # used in notfication
        source_template = client_document.source_document


        client_document
        client_document.pk = None # set the pk to null which will cause the ORM to save as a new object

        client_document.name = 'Clone of %s' % source_template.name
        client_document.meta_data = {}
        client_document.meta_data['num_signed'] = 0
        client_document.meta_data['signers'] = []
        client_document.meta_data['num_invited'] = 0
        client_document.meta_data['invitees'] = []
        client_document.save()


        url = reverse('doc:update_document', kwargs={'pk': client_document.pk})
        message = _("Cloned %s as %s") % (source_template.name, client_document.name,)

        logger.debug(message)

        # Notification
        tasks.document_cloned(source_document=source_template, document=client_document)

        return HttpResponse('[{"userdoc_id": %d, "url":"%s", "status":"%s", "message":"%s"}]' % (client_document.pk, url, 'cloned', unicode(message),), status=200, content_type="application/json")


class DeleteClientCreatedDocumentView(View):
    def post(self, request, *args, **kwargs):
        client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
        client_document.is_deleted = True
        client_document.save()
        message = _("Deleted %s, <a id='undelete-%d' class='undelete-my-document' href='%s'>undo</a>") % (client_document.name, client_document.pk, reverse('document:my_undelete', kwargs={'pk':client_document.pk}),)

        logger.debug(message)

        # Notification
        tasks.document_deleted(document=client_document)

        return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', unicode(message),), status=200, content_type="application/json")


class UndoDeleteClientCreatedDocumentView(View):
    def post(self, request, *args, **kwargs):
        client_document = get_object_or_404(ClientCreatedDocument.deleted_objects, pk=self.kwargs['pk'])
        if client_document.is_deleted is True:
            client_document.is_deleted = False
            client_document.save()
            message = _("Reactivated '%s'") % (client_document.name,)
        else:
            message = _("Was already activated '%s'") % (client_document.name,)

        logger.debug(message)

        # Notification
        tasks.document_restored(document=client_document)

        return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', message,), status=200, content_type="application/json")
