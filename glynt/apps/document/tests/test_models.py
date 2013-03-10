# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson as json
from nose.tools import *
from mocktest import *

from glynt.apps.factories import SiteFactory, DocumentFactory, DocumentHTMLFactory
from glynt.apps.document.models import ClientCreatedDocument, DocumentTemplateCategory, DocumentTemplate
from qrcode.image.pil import PilImage

import re


class TestImportedSignals(mocktest.TestCase):
    """ Ensure that the signals are imported from models.py
    which is loaded automagically by django
    """
    def test_signals_are_imported_in_models(self):
        """ Check at least 1 signal is present """
        import glynt.apps.document.models as doc_models
        assert 'generate_document_body_signal' in dir(doc_models)


class TestClientCreatedDocument(mocktest.TestCase):
    def setUp(self):
        self.name = 'Monkey Document'
        self.domain = 'http://monkey-nuts.com'
        self.doc_data = {'test_var': 1, 'monkey_var': 'Some Var'}

        self.site = SiteFactory.create(domain=self.domain)
        settings.SITE_ID = self.site.pk

        self.subject = DocumentFactory.create(name=self.name, doc_data=self.doc_data)

    def test_get_absolute_url(self):
        url = self.subject.get_absolute_url()
        eq_(re.search('/document/my/(\d+)/edit/', url) is not None, True)

    def test_get_review_url(self):
        url = self.subject.get_review_url()
        eq_(re.search('/template/my/%s/review/' % self.subject.pk, url) is not None, True)

    def test_qr_code_image(self):
        """ Test that we get a PIL image when calling this method """
        result = self.subject.qr_code_image()
        eq_(type(result), PilImage)

    def test_data_as_json(self):
        eq_(self.subject.data_as_json(), json.dumps(self.doc_data))

    def test_signatories(self):
        """ this functionality should be moved into a dedicated module """
        pass

    def test_signed_signatories(self):
        """ this functionality should be moved into a dedicated module """
        pass


class TestDocumentHTML(mocktest.TestCase):
    def setUp(self):
        self.subject = DocumentHTMLFactory.create()

    def test_render(self):
        """ need to setup Smoothe Pybars tests"""
        pass