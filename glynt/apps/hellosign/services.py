# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User

from glynt.apps.todo.models import Attachment

from bunch import Bunch
from actstream import action
# import from django-hellosign
from hellosign import HelloSign

import json
import logging
logger = logging.getLogger('lawpal.services')

from .models import Signature

HELLOSIGN_AUTHENTICATION = getattr(settings, 'HELLOSIGN_AUTHENTICATION', None)
HELLOSIGN_CLIENT_ID = getattr(settings, 'HELLOSIGN_CLIENT_ID', None)
HELLOSIGN_CLIENT_SECRET = getattr(settings, 'HELLOSIGN_CLIENT_SECRET', None)
HELLOSIGN_TEST_MODE = getattr(settings, 'HELLOSIGN_TEST_MODE', 1)

assert HELLOSIGN_AUTHENTICATION is not None, 'you must specify a HELLOSIGN_CLIENT_ID in settings.py'
assert HELLOSIGN_CLIENT_ID is not None, 'you must specify a HELLOSIGN_CLIENT_ID in settings.py'
assert HELLOSIGN_CLIENT_SECRET is not None, 'you must specify a CLIENT_SECRET in settings.py'


class HelloSignService(object):
    """
    service that communicates with hellosign
    and provides access to the functionality required
    """
    AUTHENTICATION = HELLOSIGN_AUTHENTICATION
    CLIENT_ID = HELLOSIGN_CLIENT_ID
    CLIENT_SECRET = HELLOSIGN_CLIENT_SECRET
    TEST_MODE = HELLOSIGN_TEST_MODE

    auth = None
    form = None

    def __init__(self, **kwargs):
        self.auth = None
        self.form = None

        self.api = HelloSign()

    def signers_data(self, signers):
        data = {}

        for i, signer in enumerate(signers):
            name, email = signer
            name_key, email_key = ('signers[{i}][name]'.format(i=i), 'signers[{i}][email_address]'.format(i=i),)

            data[name_key] = name
            data[email_key] = email

        return data

    def files_data(self, files):
        data = {}
        for i, file_path in enumerate(files):
            key = 'file[{i}]'.format(i=i)
            data[key] = file_path
        return data

    def send_doc_for_signing(self, form):
        """
        form: valid form object
        """
        self.form = form  # set as global form

        if form.is_valid() is False:
            raise Exception(str(form.errors))
        else:
            data = {
                'test_mode': self.TEST_MODE,
                'client_id': self.CLIENT_ID,
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            # update with signer names
            data.update(self.signers_data(signers=form.signatories()))

            files = {}
            # update with file paths
            files.update(self.files_data(files=form.documents()))

            return self.api.signature_request.create_embedded.post(auth=self.AUTHENTICATION, data=data, files=files)

    def save(self, json_data):
        if self.form is not None:

            if json_data is not None and type(json_data) is dict:

                self.form.instance.signature_request_id = json_data['signature_request_id']
                self.form.instance.data = json_data
                self.form.save()

    def update_doc_for_signing(self, signature_request_id):
        signature = Signature.objects.get(signature_request_id=signature_request_id)
        pass


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

        self.items = [Bunch(**self.payload)]

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
            event = i.event
            event_type = event.get('event_type')

            logger.info("Hellosign event: {event_date} is of type {event_type}".format(event_type=event_type, event_date=event.get('event_time',None)))

            i = self.get_class(event=event_type)(**i)

            if i is not None and hasattr(i, 'process'):
                i.process()
