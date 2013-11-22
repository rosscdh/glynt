# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Signature
from .forms import SignatureForm
from .services import HelloSignService

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=Signature, dispatch_uid='signature.on_signature_created')
def on_signature_created(sender, **kwargs):
    signature = kwargs.get('instance')

    # skip the initial create and only perform once the m2m relationships with signees is created
    if kwargs.get('created') is False:
        # only if we have more than 0 signees
        if signature.signatories.all().count() > 0:
            if signature.signature_request_id in [None, ''] and signature.is_deleted is False:
                logger.info('Sending Signature request as has no signature_request_id: pk: %d' % signature.pk)

                initial = {
                    'subject': signature.data.get('subject', 'Hi there, I\'d like to invite you to sign this document'),
                    'message': signature.data.get('message', 'This is to test the HelloSign singature process'),
                    'requested_by': signature.requested_by.pk,
                    'document': signature.document.pk,
                    'signatories': [s.pk for s in signature.signatories.all()],
                    'project': signature.document.todo.project.pk,
                    'signature_request_id': None,
                    'is_complete': False,
                    'is_deleted': False,
                }

                form = SignatureForm(user=signature.requested_by, data=initial, instance=signature)

                service = HelloSignService()

                service.process(form=form)
            else:
                logger.info('Not Sending Signature request as already has signature_request_id: pk: %d %s' % (signature.pk, signature.signature_request_id))