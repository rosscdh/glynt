# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatewords
from django.contrib.comments.models import Comment

from glynt.apps.document import tasks
from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument
from glynt.apps.services.services import BasePdfService


@receiver(post_save, sender=DocumentTemplate, dispatch_uid='template.html.validate')
def validate_template_html(sender, **kwargs):
    template = kwargs['instance']
    # open html and render body
    html_service = BasePdfService(template='export/xhtml_validator.html', html=template.body)
    # Validate HTML
    tasks.validate_document_html(html=html_service.get_html())


@receiver(post_save, sender=Comment)
def save_document_comment_signal(sender, **kwargs):
    comment = kwargs['instance']
    client_document = ClientCreatedDocument.objects.get(pk=comment.object_pk)
    source_document = client_document.source_document
    comment_text = truncatewords(comment.comment, 15)
    # Notification
    tasks.document_comment(source_document=source_document, document=client_document, commenting_user=comment.user, commenting_user_name=comment.user_name, comment=comment_text)


@receiver(post_save, sender=ClientCreatedDocument, dispatch_uid='document.html.generate')
def generate_document_body_signal(sender, **kwargs):
    document = kwargs['instance']
    # Generate HTML Body
    tasks.generate_document_html(document=document)


