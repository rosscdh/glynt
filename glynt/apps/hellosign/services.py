# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from glynt.apps.todo.models import Attachment

from bunch import Bunch
from actstream import action

# import from django-hellosign
from hellosign import HelloSign
import crocodoc as crocdoc

import os
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

CROCDOC_API_KEY = getattr(settings, 'CROCDOC_API_KEY', None)
if CROCDOC_API_KEY is None:
    raise Exception("You must specify a CROCDOC_API_KEY in your local_settings.py")

crocdoc.api_token = CROCDOC_API_KEY


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
    files = {}

    def __init__(self, **kwargs):

        self.auth = None
        self.form = None
        files = {}

        self.api = HelloSign()

    def signers_data(self, signers):
        data = {}

        for i, signer in enumerate(signers):
            name, email = (signer.get_full_name(), signer.email)
            name_key, email_key = ('signers[{i}][name]'.format(i=i), 'signers[{i}][email_address]'.format(i=i),)

            data[name_key] = name
            data[email_key] = email

        return data

    def files_data(self, files):
        data = {}

        for i, file_item in enumerate(files):
            # doanload from crocdoc and store locally
            storage = FileSystemStorage()
            crocdoc_uuid = file_item.crocdoc_uuid
            # download from crocdoc
            crocdoc_file = crocdoc.download.document(crocdoc_uuid, pdf=True, annotated=False, user_filter=None)
            # store the file and get name
            stored_file = storage.save(name='sign/{name}.pdf'.format(name=crocdoc_uuid), content=ContentFile(crocdoc_file))
            # get full path so that we can send that off to hellosign
            file_path = '{base}/{file_path}'.format(base=storage.location, file_path=stored_file)

            key = 'file[{i}]'.format(i=i)  # crappy php/curl style names
            data[key] = file_path  # save path in key

        return data

    def send_doc_for_signing(self, form):
        """
        form: valid form object
        """
        self.form = form  # set as global form

        if form.is_valid() is not True:
            raise Exception(str(form.errors))
        else:
            data = {
                'test_mode': self.TEST_MODE,
                'client_id': self.CLIENT_ID,
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            # update with signer names
            data.update(self.signers_data(signers=form.cleaned_data.get('signatories', [])))

            self.files = {}
            # update with file paths
            self.files.update(self.files_data(files=[form.cleaned_data.get('document')]))

            return self.api.signature_request.create_embedded.post(auth=self.AUTHENTICATION, data=data, files=self.files)

    def cleanup(self):
        for filepath in self.files.values():
            os.remove(filepath)
        self.files = {}

    def save(self, json_data):
        if self.form is not None:
            if type(json_data) is dict:

                self.form.instance.signature_request_id = json_data['signature_request_id']
                self.form.instance.data.update(json_data)
                self.form.save()

    def process(self, form):
        resp = self.send_doc_for_signing(form=form)
        self.save(json_data=resp.json().get('signature_request'))  # saves the signature_request as flat data!
        self.cleanup();

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
            full_name, email = self.owner.split(',')
            self._user = User.objects.get(email=email)
        return self._user

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
                        action_object=self.doc,
                        target=self.doc.todo,
                        attachment_name=self.doc.filename)
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
    _user = None
    _doc = None
    signature = None
    items = []

    def __init__(self, payload=payload, *args, **kwargs):
        self._user = None
        self.signature = None
        self.payload = json.loads(payload)
        
        if 'signature_request' in self.payload:
            signature_request_id = self.payload['signature_request']['signature_request_id']

            try:
                self.signature = Signature.objects.get(signature_request_id=signature_request_id)
                self._user = self.signature.requested_by
                self._doc = self.signature.document

            except Signature.DoesNotExist as e:
                self.signature = None
                logger.critical('HelloSign Signature does not exist: %s' % signature_request_id)

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
        if self.signature is not None and self._user is not None:

            for c, i in enumerate(self.items):
                event = i.event
                event_type = event.get('event_type')

                logger.info("Hellosign event: {event_date} is of type {event_type}".format(event_type=event_type, event_date=event.get('event_time',None)))

                i._user = self._user # set out owner to that of the file
                i.doc = self._doc
                i = self.get_class(event=event_type)(**i)

                if i is not None and hasattr(i, 'process'):
                    i.process()
