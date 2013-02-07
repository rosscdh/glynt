# -*- coding: utf-8 -*-
from django.conf import settings
from nose.tools import *
from mocktest import *

from .services import GlyntPdfService, HelloSignService
from glynt.apps.factories import DocumentFactory

import re


class TestGlyntPdfService(mocktest.TestCase):
    def setUp(self):
        self.html = '<h1>Document Title</h1><p>Hi there</p>'
        self.title = 'Title Goes Here'
        self.subject = GlyntPdfService(html=self.html, title=self.title)

    @raises(TypeError)
    def test_init_fail(self):
        subject = GlyntPdfService()

        signature = HelloSignSignature(title='title', subject='My Subject', message='My Message')
        signature.add_signer(HelloSigner(email='sendrossemail@gmail.com', name='Bob Examplar'))
        signature.add_signer(HelloSigner(email='sendrossemail+2@gmail.com', name='Bob Examplar2'))
        signature.add_doc(HelloDoc(file_path='/home/rossc/Projects/AboutStacks.pdf'))
        r = signature.create(auth=authentication)


class TestHelloSignService(mocktest.TestCase):
    def setUp(self):
        self.document = DocumentFactory.create()
        self.invitees = [{'name': 'John Doe', 'email_address': 'John@lawpal.com'}]
        self.subject = HelloSignService(document=self.document, invitees=self.invitees)

    @raises(TypeError)
    def test_init_fail(self):
        subject = HelloSignService()

    def test_random_filename(self):
        filename = self.subject.random_filename()
        assert settings.MEDIA_ROOT in filename
        assert '.pdf' in filename
        assert '%d-'%(self.document.pk,) in filename
        # must contain a string like /2-bd89414c8a687cb6b4508952a8621dfc.pdf
        assert re.search('\/(\d+)\-([a-z0-9]+)\.pdf', filename) is not None
