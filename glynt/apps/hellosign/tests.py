"""
"""
from django.db import transaction
from django.test import TestCase
from hellosign import HelloSign

from model_mommy import mommy
import mock
import json

from .forms import SignatureForm
from .services import HelloSignService

REQUESTED_BY = mommy.make('auth.User', username='requestor', email='test+requestor@lawpal.com')
SIGNATORIES = [mommy.make('auth.User', username='signatory-%d' % i, email='test+signatory_%d@lawpal.com' % i) for i in range(2,5)]
PROJECT = mommy.make('project.Project')

EXPECTED_DOC_UUID = '777666555444333222111000'

EXPECTED_SIGNATURES = [{u'signed_at': None, u'status_code': u'awaiting_signature', u'last_viewed_at': None, u'signer_email_address': s.email, u'signer_name': s.get_full_name(), u'last_reminded_at': None, u'signature_id': u'fd6d39525f3ef3da3069d038d3f9e1df', u'order': None} for s in SIGNATORIES]


def post(self, **kwargs):
    import pdb;pdb.set_trace()
    return json.dumps({u'signature_request': {u'test_mode': True, u'cc_email_addresses': [], u'title': kwargs.get('subject'), u'signature_request_id': '123456789-987654321', u'original_title': kwargs.get('subject'), u'requester_email_address': u'founders@lawpal.com', u'details_url': u'https://www.hellosign.com/home/manage?locate=%s' % EXPECTED_DOC_UUID, u'signing_url': u'https://www.hellosign.com/editor/sign?guid=%s' % EXPECTED_DOC_UUID, u'has_error': False, u'signatures': EXPECTED_SIGNATURES, u'response_data': [], u'message': kwargs.get('message'), u'is_complete': False, u'custom_fields': [], u'subject': kwargs.get('subject')}})


class HelloSignServiceTest(TestCase):

    def setUp(self):
        super(HelloSignServiceTest, self).setUp()

        self.subject = HelloSignService()
        self.REQUESTED_BY = REQUESTED_BY
        self.SIGNATORIES = SIGNATORIES
        self.PROJECT = PROJECT

    @mock.patch('hellosign.HelloSign.post', post)
    def test_send_doc_for_signing(self):
        """
        """
        initial = {
            'subject': 'Hi there, I\'d like to invite you to sign this document',
            'message': 'This is to test the HelloSign singature process',
            'requested_by': self.REQUESTED_BY.pk,
            'signatories': [s.pk for s in self.SIGNATORIES],
            'project': self.PROJECT.pk,
            'data': {},
            'signature_request_id': None,
            'is_complete': False,
        }
        form = SignatureForm(user=REQUESTED_BY, data=initial)
        resp = self.subject.send_doc_for_signing(form=form)
        self.subject.save()
        import pdb;pdb.set_trace()
