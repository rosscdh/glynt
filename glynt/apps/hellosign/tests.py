"""
"""
from django.test import TestCase

from model_mommy import mommy
import mock
import json

from .models import Signature
from .forms import SignatureForm
from .services import HelloSignService


class HelloSignServiceTest(TestCase):
    """
    Test the flow of the Hellosign send for signature
    Mockout the actual requests
    Use the provided SignatureForm + HelloSignService flow
    """
    def setUp(self):
        super(HelloSignServiceTest, self).setUp()

        self.subject = HelloSignService()
        self.REQUESTED_BY = mommy.make('auth.User', email='test+requestor@lawpal.com')
        self.SIGNATORIES = [mommy.make('auth.User', email='test+signatory_%d@lawpal.com' % i) for i in range(2, 5)]
        self.PROJECT = mommy.make('project.Project')

        self.EXPECTED_SIGNATURE_REQUEST_ID = '123456789-987654321'
        self.EXPECTED_DOC_UUID = '777666555444333222111000'

        self.EXPECTED_SIGNATURES = [{u'signed_at': None, u'status_code': u'awaiting_signature', u'last_viewed_at': None, u'signer_email_address': s.email, u'signer_name': s.get_full_name(), u'last_reminded_at': None, u'signature_id': u'fd6d39525f3ef3da3069d038d3f9e1df', u'order': None} for s in self.SIGNATORIES]

    def tearDown(self):
        """
        remove the junk data
        """
        super(HelloSignServiceTest, self).tearDown()
        for u in [self.REQUESTED_BY] + self.SIGNATORIES:
            u.delete()
        self.PROJECT.delete()

    def test_send_doc_for_signing(self):
        # Setup constants for use in the mock
        REQUESTED_BY = self.REQUESTED_BY

        EXPECTED_SIGNATURE_REQUEST_ID = self.EXPECTED_SIGNATURE_REQUEST_ID
        EXPECTED_DOC_UUID = self.EXPECTED_DOC_UUID

        EXPECTED_SIGNATURES = self.EXPECTED_SIGNATURES

        # the mocked hello signpost needs to be done here due to constants
        def hellosign_post(self, **kwargs):

            # a fake request object to emulate https://github.com/kennethreitz/requests/blob/master/requests/models.py Request
            class Request(object):
                """
                Faked python requests Response model
                """
                @property
                def content(self):
                    return json.dumps(self.json())

                def json(self):
                    """
                    return mocked Hellosign Response
                    """
                    return {u'signature_request': {u'test_mode': True, u'cc_email_addresses': [], u'title': kwargs.get('subject'), u'signature_request_id': EXPECTED_SIGNATURE_REQUEST_ID, u'original_title': kwargs.get('subject'), u'requester_email_address': u'founders@lawpal.com', u'details_url': u'https://www.hellosign.com/home/manage?locate=%s' % EXPECTED_DOC_UUID, u'signing_url': u'https://www.hellosign.com/editor/sign?guid=%s' % EXPECTED_DOC_UUID, u'has_error': False, u'signatures': EXPECTED_SIGNATURES, u'response_data': [], u'message': kwargs.get('message'), u'is_complete': False, u'custom_fields': [], u'subject': kwargs.get('subject')}}
            return Request()

        # mock out the post event
        with mock.patch('hellosign.HelloSign.post', hellosign_post):
            initial = {
                'subject': 'Hi there, I\'d like to invite you to sign this document',
                'message': 'This is to test the HelloSign singature process',
                'requested_by': self.REQUESTED_BY.pk,
                'signatories': [s.pk for s in self.SIGNATORIES],
                'project': self.PROJECT.pk,
                'signature_request_id': None,
                'is_complete': False,
            }
            form = SignatureForm(user=REQUESTED_BY, data=initial)

            resp = self.subject.send_doc_for_signing(form=form)

            self.subject.save(json_data=resp.json().get('signature_request'))  # saves the signature_request as flat data!

            signature = Signature.objects.get(signature_request_id=EXPECTED_SIGNATURE_REQUEST_ID)

            self.assertTrue(signature is not None)
            self.assertEqual(signature.details_url, 'https://www.hellosign.com/home/manage?locate=777666555444333222111000')
            self.assertEqual(signature.signing_url, 'https://www.hellosign.com/editor/sign?guid=777666555444333222111000')
