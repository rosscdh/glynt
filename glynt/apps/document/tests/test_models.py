# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson as json
from nose.tools import *
from mocktest import *

from glynt.apps.factories import SiteFactory, DocumentFactory, DocumentHTMLFactory
from glynt.apps.document.models import DocumentHTML, ClientCreatedDocument, DocumentTemplateCategory, DocumentTemplate
from qrcode.image.pil import PilImage

import re
import pdb


class TestImportedSignals(mocktest.TestCase):
    def test_signals_are_imported_in_models(self):
        import glynt.apps.document.models as doc_models
        assert 'generate_document_body_signal' in dir(doc_models)


class TestClientCreatedDocument(mocktest.TestCase):
    def setUp(self):
        self.slug = 'monkey-document'
        self.name = 'Monkey Document'
        self.domain = 'http://monkey-nuts.com'
        self.doc_data = {'test_var': 1, 'monkey_var': 'Some Var'}

        self.site = SiteFactory.create(domain=self.domain)
        settings.SITE_ID = self.site.pk

        self.subject = DocumentFactory.create(name=self.name, slug=self.slug, doc_data=self.doc_data)

    def test_get_absolute_url(self):
        url = self.subject.get_absolute_url()
        assert re.search('/v2/doc/my/(\d+)/edit/', url) is not None

    def test_get_review_url(self):
        url = self.subject.get_review_url()
        assert re.search('/doc/my/%s/review/'%(self.slug,), url) is not None

    def test_qr_code_image(self):
        result = self.subject.qr_code_image()
        assert type(result) == PilImage

    def test_increment_num_signed(self):
        """ SIGNED """
        self.subject.increment_num_signed(4)
        assert self.subject.meta_data['num_signed'] == 1

        for i in range(1,5):
            self.subject.increment_num_signed(i)
        # is 24 and not 25 because we added signature_id 1 which is then already in the model
        assert self.subject.meta_data['num_signed'] == 4

    def test_increment_num_invited(self):
        """ INVITED """
        self.subject.increment_num_invited(4)
        assert self.subject.meta_data['num_invited'] == 1

        for i in range(1,5):
            self.subject.increment_num_invited(i)
        # is 24 and not 25 because we added signature_id 1 which is then already in the model
        assert self.subject.meta_data['num_invited'] == 4

    def test_signatories(self):
        pass

    def test_signed_signatories(self):
        pass

    def test_data_as_json(self):
        assert self.subject.data_as_json() == json.dumps(self.doc_data)


class TestDocumentHTML(mocktest.TestCase):
    def setUp(self):
        self.subject = DocumentHTMLFactory.create()

    def test_render(self):
        """ need to setup Smoothe Pybars tests"""
        pass