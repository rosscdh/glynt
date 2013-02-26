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


class BaseService(mocktest.TestCase):
    def setUp(self):
        self.document = DocumentFactory.create()
        self.user = UserFactory.create()
        self.key_hash = hashlib.md5()

        self.meta_data = {
          'to_name': 'Monkey Nuts',
          'to_email': 'test-monkey@lawpal.com',
          'invited_by_pk': 1,
          'invited_by_name': 'Test Invitor',
          'invited_by_email': 'test-invitor@lawpal.com'
        }

        # cheekey.. please note.. using .build (does not save the sig) and manually setting pk so we cant test for unique id
        self.signature = SignatureFactory.build(pk=1, document=self.document, meta_data=self.meta_data, user=self.user)


class TestDocumentSignerService(BaseService):
    def setUp(self):
        super(TestDocumentSignerService, self).setUp()
        self.signature.is_signed = True
        self.subject = DocumentSignerService(document=self.document)
        self.subject.reset()

    @raises(TypeError)
    def test_bad_init(self):
        """ throws error TypeError: __init__() takes 
        exactly 2 arguments (1 given) """
        DocumentSignerService()

    def test_increment(self):
        self.subject.increment(self.signature)

        eq_(self.document.meta_data['num_signed'], 1)
        eq_(type(self.document.meta_data['signers']), list)
        eq_(self.signature.pk in self.document.meta_data['signers'], True)
        eq_(len(self.document.meta_data['signers']), 1)

    def test_decrement(self):
        # add 1
        self.subject.increment(self.signature)
        # then take it away
        self.subject.decrement(self.signature)

        eq_(self.document.meta_data['num_signed'], 0)
        eq_(type(self.document.meta_data['signers']), list)
        eq_(self.signature.pk not in self.document.meta_data['signers'], True)
        eq_(len(self.document.meta_data['signers']), 0)

    def test_same_signature_increment_range(self):
        """ 
        When trying to add the same signature the incrementor 
        should only increment once
        """
        s = self.signature
        self.subject.increment(s)

        for i in range(1,5):
            s.key_hash = self.key_hash.update(str(datetime.datetime.utcnow()))
            self.subject.increment(s)

        eq_(self.document.meta_data['num_signed'], 1)

    def test_increment_range(self):
        s = self.signature
        for i in range(0,3):
            # Make a new signature
            s.pk = i
            s.is_signed = True
            self.key_hash.update(str(random.random()))
            s.key_hash = self.key_hash.hexdigest()
            self.subject.increment(s)

        eq_(self.document.meta_data['num_signed'], 3)


class TestDocumentInviteeService(BaseService):
    def setUp(self):
        super(TestDocumentInviteeService, self).setUp()
        self.subject = DocumentInviteeService(document=self.document)
        self.subject.reset()

    @raises(TypeError)
    def test_bad_init(self):
        """ throws error TypeError: __init__() takes 
        exactly 2 arguments (1 given) """
        DocumentInviteeService()

    def test_increment(self):
        self.subject.increment(self.signature)

        eq_(self.document.meta_data['num_invited'], 1)
        eq_(type(self.document.meta_data['invitees']), list)
        eq_(self.signature.pk in self.document.meta_data['invitees'], True)
        eq_(len(self.document.meta_data['invitees']), 1)

    def test_decrement(self):
        # add 1
        self.subject.increment(self.signature)
        # then take it away
        self.subject.decrement(self.signature)

        eq_(self.document.meta_data['num_invited'], 0)
        eq_(type(self.document.meta_data['invitees']), list)
        eq_(self.signature.pk not in self.document.meta_data['invitees'], True)
        eq_(len(self.document.meta_data['invitees']), 0)

    def test_same_signature_increment_range(self):
        """ 
        When trying to add the same signature the incrementor 
        should only increment once
        """
        s = self.signature
        for i in range(1,5):
            s.key_hash = self.key_hash.update(str(datetime.datetime.utcnow()))
            self.subject.increment(s)

        eq_(self.document.meta_data['num_invited'], 1)

    def test_increment_range(self):
        s = self.signature
        for i in range(0,3):
            # Make a new signature
            s.pk = i
            self.key_hash.update(str(random.random()))
            s.key_hash = self.key_hash.hexdigest()
            self.subject.increment(s)

        eq_(self.document.meta_data['num_invited'], 3)