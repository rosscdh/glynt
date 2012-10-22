# -*- coding: utf-8 -*-
# signals to handle the sending of signature invitations, when a new DocumentSignature model is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatewords
from django.contrib.comments.models import Comment

from glynt.apps.document import tasks
from glynt.apps.document.models import ClientCreatedDocument

import datetime



@receiver(post_save, sender=Comment)
def save_document_comment_signal(sender, **kwargs):
    comment = kwargs['instance']
    client_document = ClientCreatedDocument.objects.get(pk=comment.object_pk)
    source_document = client_document.source_document
    comment_text = truncatewords(comment.comment, 15)
    # Notification
    tasks.document_comment(source_document=source_document, document=client_document, commenting_user=comment.user, commenting_user_name=comment.user_name, comment=comment_text)