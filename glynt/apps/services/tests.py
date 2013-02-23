# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from nose.tools import *
from mocktest import *

from .services import GlyntPdfService, GlyntDocxService, HelloSignService
from glynt.apps.services.services import BaseService
from hellosign import HelloSignSignature, HelloSigner
from glynt.apps.factories import DocumentFactory

import re


class TestBaseService(mocktest.TestCase):
    def setUp(self):
        self.html = '<h1>Document Title</h1><p>Hi there</p>'
        self.title = 'Title Goes Here'
        self.subject = BaseService(html=self.html, title=self.title)

    @raises(TypeError)
    def test_init_fail(self):
        subject = BaseService()

    def test_template(self):
        assert self.subject.template == 'export/pdf.html'

    def test_get_context(self):
        context = self.subject.get_context()
        assert 'title' in context
        assert 'body' in context
        assert context['title'] == self.title
        assert context['body'] == self.html

    def test_get_html(self):
        context = self.subject.get_context()
        result = self.subject.get_html(context)
        assert '<html>' in result
        assert '</html>' in result
        assert '<body>' in result
        assert '</body>' in result
        assert '<title>%s</title>'%(self.title,) in result
        assert context['body'] in result


class TestGlyntPdfService(mocktest.TestCase):
    def setUp(self):
        self.html = '<h1>Document Title</h1><p>Hi there</p>'
        self.title = 'Title Goes Here'
        self.subject = GlyntPdfService(html=self.html, title=self.title)

    @raises(TypeError)
    def test_init_fail(self):
        subject = GlyntPdfService()

    def test_create_pdf(self):
        result = self.subject.create_pdf()
        assert result.name is not None
        assert type(result) is ContentFile
        assert result._size > 0


class TestHelloSignService(mocktest.TestCase):
    def setUp(self):
        self.document = DocumentFactory.create()
        self.invitees = [{'name': 'John Doe', 'email': 'John@lawpal.com'}, {'name': 'Joe Schmoe', 'email': 'Joe@lawpal.com'}]

        # Mock Signature which is dependency injected
        HelloSignSignatureClass = HelloSignSignature
        when(HelloSignSignatureClass).create.then_return({'result':'success'}) # Totally faked out result
        when(HelloSignSignatureClass).add_signer.then_return(True)
        when(HelloSignSignatureClass).add_doc.then_return(True)

        self.subject = HelloSignService(document=self.document, invitees=self.invitees, HelloSignSignatureClass=HelloSignSignatureClass)

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

    def test_create_pdf_expectations(self):
        expect(self.subject.HelloSignSignatureClass).add_signer.exactly(2).times() # there are 2 invitees in setUp
        expect(self.subject.HelloSignSignatureClass).add_doc.once()
        expect(self.subject.HelloSignSignatureClass).create.once()
        self.subject.send_for_signing()

    def test_create_pdf(self):
        result = self.subject.send_for_signing()
        assert result == {'result':'success'}
