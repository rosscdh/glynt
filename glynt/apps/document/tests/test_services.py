# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson as json
from nose.tools import *
from mocktest import *

from glynt.apps.factories import UserFactory, TemplateFactory, DocumentFactory, SignatureFactory, DocumentHTMLFactory
from glynt.apps.document.services import DocumentSignerService, DocumentInviteeService

import hashlib
import datetime
import random
import pdb

class BaseService(mocktest.TestCase):
    def setUp(self):
        self.document = DocumentFactory.create()

        self.key_hash = hashlib.md5()

        self.meta_data = {
          'to_name': 'Monkey Nuts',
          'to_email': 'test-monkey@lawpal.com',
          'invited_by_pk': 1,
          'invited_by_name': 'Test Invitor',
          'invited_by_email': 'test-invitor@lawpal.com'
        }

        self.signature = SignatureFactory.create(document=self.document, meta_data=self.meta_data)


class TestDocumentSignerService(BaseService):
    def setUp(self):
        super(TestDocumentSignerService, self).setUp()
        self.subject = DocumentSignerService(document=self.document)

    @raises(TypeError)
    def test_bad_init(self):
        """ throws error TypeError: __init__() takes 
        exactly 2 arguments (1 given) """
        DocumentSignerService()

    def test_increment(self):
        self.subject.increment(self.signature)

        assert self.document.meta_data['num_signed'] == 1
        assert type(self.document.meta_data['signers']) == list
        assert self.signature.pk in self.document.meta_data['signers']
        assert len(self.document.meta_data['signers']) == 1

    def test_decrement(self):
        # add 1
        self.subject.increment(self.signature)
        # then take it away
        self.subject.decrement(self.signature)

        assert self.document.meta_data['num_signed'] == 0
        assert type(self.document.meta_data['signers']) == list
        assert self.signature.pk not in self.document.meta_data['signers']
        assert len(self.document.meta_data['signers']) == 0

    def test_same_signature_increment_range(self):
        """ 
        When trying to add the same signature the incrementor 
        should only increment once
        """
        s = self.signature
        for i in range(1,5):
            s.key_hash = self.key_hash.update(str(datetime.datetime.utcnow()))
            self.subject.increment(s)

        assert self.document.meta_data['num_signed'] == 1

    def test_increment_range(self):
        s = mock('mockSignature')
        for i in range(1,3):
            # Make a new signature
            s.pk = i
            self.key_hash.update(str(random.random()))
            s.key_hash = self.key_hash.hexdigest()
            self.subject.increment(s)

        assert self.document.meta_data['num_signed'] == 2


class TestDocumentInviteeService(BaseService):
    def setUp(self):
        super(TestDocumentInviteeService, self).setUp()
        self.subject = DocumentInviteeService(document=self.document)

    @raises(TypeError)
    def test_bad_init(self):
        """ throws error TypeError: __init__() takes 
        exactly 2 arguments (1 given) """
        DocumentInviteeService()

    def test_increment(self):
        self.subject.increment(self.signature)

        assert self.document.meta_data['num_invited'] == 1
        assert type(self.document.meta_data['invitees']) == list
        assert self.signature.pk in self.document.meta_data['invitees']
        assert len(self.document.meta_data['invitees']) == 1

    def test_decrement(self):
        # add 1
        self.subject.increment(self.signature)
        # then take it away
        self.subject.decrement(self.signature)

        assert self.document.meta_data['num_invited'] == 0
        assert type(self.document.meta_data['invitees']) == list
        assert self.signature.pk not in self.document.meta_data['invitees']
        assert len(self.document.meta_data['invitees']) == 0

    def test_same_signature_increment_range(self):
        """ 
        When trying to add the same signature the incrementor 
        should only increment once
        """
        s = self.signature
        for i in range(1,5):
            s.key_hash = self.key_hash.update(str(datetime.datetime.utcnow()))
            self.subject.increment(s)

        assert self.document.meta_data['num_invited'] == 1

    def test_increment_range(self):
        s = mock('mockSignature')
        for i in range(1,3):
            # Make a new signature
            s.pk = i
            self.key_hash.update(str(random.random()))
            s.key_hash = self.key_hash.hexdigest()
            self.subject.increment(s)

        assert self.document.meta_data['num_invited'] == 3