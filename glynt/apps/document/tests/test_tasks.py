# -*- coding: utf-8 -*-
from nose.tools import *
from mocktest import *
from glynt.apps.factories import DocumentFactory, DocumentHTMLFactory
from glynt.apps.document.models import DocumentHTML
from glynt.apps.services import GlyntPdfService

from glynt.apps.document.tasks import document_created_task, document_deleted_task, document_restored_task, \
                        document_cloned_task, document_comment_task, generate_document_html_task, convert_to_pdf_task
import user_streams


class TestDocumentTasks(mocktest.TestCase):
    def setUp(self):
        self.document = DocumentFactory.create()

    def test_document_created(self):
        #expect(user_streams).add_stream_item.once()
        expect(self.document).get_absolute_url.once()
        # test
        document_created_task(document=self.document)

    def test_document_deleted(self):
        #expect(user_streams).add_stream_item.once()
        # test
        document_deleted_task(document=self.document)

    def test_document_restored(self):
        #expect(user_streams).add_stream_item.once()
        # test
        document_restored_task(document=self.document)

    def test_document_cloned(self):
        #expect(user_streams).add_stream_item.once()
        # test
        document_cloned_task(source_document=self.document.source_document, document=self.document)

    def test_document_comment(self):
        #expect(user_streams).add_stream_item.once()
        #expect(self.document.owner).get_full_name.exactly(2).times()
        # test
        document_comment_task(commenting_user=self.document.owner, commenting_user_name=self.document.owner.get_full_name(), document=self.document, comment='My Comment')

    def test_generate_document_html(self):
        doc_html = DocumentHTMLFactory.create(document=self.document)
        expect(DocumentHTML.objects).get_or_create(document=self.document).once()
        when(DocumentHTML.objects).get_or_create.then_return((doc_html, True,))
        expect(doc_html).save.once()
        # test
        generate_document_html_task(document=self.document)

    def test_convert_to_pdf(self):
        pass
    #     """ e
    #         @TODO this is a POC
    #         >>> # Send for HTML to PDF conversion
    #         >>> convert_to_pdf(document_html=html, title=document.name)
    #     """
    #     logger.info('Creating PDF Document: %s DocumentHTML: %s'%(kwargs.get('document_pk', None), kwargs.get('document_html_pk', None),))
    #     glynt_pdf = GlyntPdfService(html=document_html.render(), title=kwargs.get('title', None))
    #     pdf_file = glynt_pdf.create_pdf()
    #     default_storage.save('%s/glyntpdf.pdf'%(settings.MEDIA_ROOT,), pdf_file)
