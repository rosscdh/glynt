# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from glynt.apps.todo.models import Attachment

from bunch import Bunch
from actstream import action

import json
import logging
logger = logging.getLogger('lawpal.services')


class HelloSignBaseEvent(Bunch):
    _verb = None
    _deleted_verb = None
    _user = None
    _attachment = None
    label = 'HelloSign Webhook Callback'
    content = None
    event = None
    type = None
    owner = None
    page = None
    doc = None
    uuid = None

    def __init__(self, *args, **kwargs):
        super(HelloSignBaseEvent, self).__init__(*args, **kwargs)
        self.__dict__.update(kwargs)

    @property
    def user(self):
        """ HelloSign provides userid as string(pk,user_name)"""
        if self._user is None:
            pk, full_name = self.owner.split(',')
            pk = int(pk)
            self._user = User.objects.get(pk=pk)
        return self._user

    @property
    def attachment(self):
        if self._attachment is None:
            self._attachment = Attachment.objects.get(uuid=self.doc)
        return self._attachment

    @property
    def verb(self):
        if 'delete' in self.event:
            return self._deleted_verb
        else:
            return self._verb

    def process(self):
        try:
            action.send(self.user, 
                        verb=self.verb,
                        action_object=self.attachment, 
                        target=self.attachment.todo,
                        attachment_name=self.attachment.filename,
                        **self.toDict())
        except Exception as e:
            logger.error('There was an exception with the HelloSignWebhookService: {error}'.format(error=e))

"""
http://www.hellosign.com/api/reference#events
signature_request_viewed    The SignatureRequest has been viewed.   SignatureRequest
signature_request_signed    A signer has completed all required fields on the SignatureRequest. SignatureRequest
signature_request_sent  The SignatureRequest has been sent successfully.    SignatureRequest
signature_request_all_signed    All signers have completed all required fields for the SignatureRequest and the final PDF is ready to be downloaded using signature_request/final_copy. SignatureRequest
file_error  We're unable to convert the file you provided.  SignatureRequest
"""
class HelloSignSignatureRequestViewed(HelloSignBaseEvent):
    _verb = 'The SignatureRequest has been viewed'


class HelloSignSignatureRequestSigned(HelloSignBaseEvent):
    _verb = 'A signer has completed all required fields on the SignatureRequest'


class HelloSignSignatureRequestSent(HelloSignBaseEvent):
    _verb = 'The SignatureRequest has been sent successfully'


class HelloSignSignatureRequestAllSigned(HelloSignBaseEvent):
    _verb = 'All signers have completed all required fields for the SignatureRequest and the final PDF is ready to be downloaded using signature_request/final_copy'


class HelloSignFileError(HelloSignBaseEvent):
    _verb = 'HelloSign is unable to convert the file provided'


class HelloSignWebhookService(object):
    payload = None

    def __init__(self, payload=payload, *args, **kwargs):
        self.user = kwargs.get('user')
        self.payload = json.loads(payload)
        self.items = [Bunch(**i) for i in self.payload]

    @property
    def class_map(self):
        return {
            'signature_request_viewed': HelloSignSignatureRequestViewed,
            'signature_request_signed': HelloSignSignatureRequestSigned,
            'signature_request_sent': HelloSignSignatureRequestSent,
            'signature_request_all_signed': HelloSignSignatureRequestAllSigned,
            'file_error': HelloSignFileError,
        }

    def get_class(self, event):
        try:
            return self.class_map[event]
        except:
            logger.error('No HelloSign Event class was found called %s' % event)
            return None

    def process(self):
        page = None
        for c, i in enumerate(self.items):
            #print '{num}: Item: {i}'.format(num=c, i=i)
            event = i.get('event')
            event_type = i.get('type')
            if i.get('page') is not None:
                page = i.get('page')

            logger.info("{event} is of type {event_type} on page: {page}".format(event_type=event_type, event=event, page=page))

            i = self.get_class()(**i)

            if i is not None and hasattr(i, 'process'):
                i.process()
