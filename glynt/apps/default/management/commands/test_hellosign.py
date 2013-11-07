# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from hellosign import HelloSign

import requests

AUTHENTICATION = ("founders@lawpal.com", "test2007")

CLIENT_ID = '9bc892af173754698e3fa30dedee3826'
CLIENT_SECRET = '8d770244b9971abfe789f5224552239d'


class Command(BaseCommand):
    help = 'Testign the hellosign api'

    def handle(self, *args, **options):
        #self.account_info()
        #self.oauth_authorize()
        #self.upload_doc_for_signing()
        self.signature_url()

    def account_info(self):
        # Account info
        resp = HelloSign().account.get(auth=AUTHENTICATION)
        print resp
        import pdb;pdb.set_trace()
        
    def oauth_authorize(self):
        # Authorize Url # https://www.hellosign.com/oauth/authorize?response_type=code&client_id=9bc892af173754698e3fa30dedee3826&state=02a263f8
        resp = requests.get('https://api.hellosign.com/oauth/authorize', params={'response_type': 'code', 'client_id': '9bc892af173754698e3fa30dedee3826', 'state': '02a263f8'})  # Raw
        # req = HelloSign()
        # req.base_uri = 'https://www.hellosign.com/oauth/authorize'
        # data = {
        #             'response_type': 'code',
        #             'client_id': CLIENT_ID,
        #             'state': '02a263f8'
        #         }
        # resp = req.oauth.authorize.get(auth=AUTHENTICATION, **data)
        import pdb;pdb.set_trace()

    def upload_doc_for_signing(self):
        # Upload a document and create embedded signing element
        data = {
            'test_mode': 1,
            'client_id': CLIENT_ID,
            'subject': 'Second test document',
            'message': 'Yay working?',
            'signers[0][name]': 'Ross C',
            'signers[0][email_address]': 'ross@lawpal.com',
            'signers[1][name]': 'Alex H',
            'signers[1][email_address]': 'alex@lawpal.com',
        }
        files = {
            'file[0]': open('/Users/rosscdh/Projects/lawpal/glynt/glynt/casper/test.pdf')
        }
        #resp = requests.post('https://api.hellosign.com/v3/signature_request/create_embedded', auth=AUTHENTICATION, data=data, files=files) # Raw
        resp = HelloSign().signature_request.create_embedded.post(auth=AUTHENTICATION, data=data, files=files)
        print resp.json()
        # returns
        #{u'signature_request': {u'test_mode': True, u'cc_email_addresses': [], u'title': u'First test document', u'signature_request_id': u'666689eee9c9b3a639eb2cb550a02e0dcea7f07d', u'original_title': u'First test document', u'requester_email_address': u'founders@lawpal.com', u'details_url': u'https://www.hellosign.com/home/manage?locate=666689eee9c9b3a639eb2cb550a02e0dcea7f07d', u'signing_url': u'https://www.hellosign.com/editor/sign?guid=666689eee9c9b3a639eb2cb550a02e0dcea7f07d', u'has_error': False, u'signatures': [{u'signed_at': None, u'status_code': u'awaiting_signature', u'last_viewed_at': None, u'signer_email_address': u'ross@lawpal.com', u'signer_name': u'Ross C', u'last_reminded_at': None, u'signature_id': u'fd6d39525f3ef3da3069d038d3f9e1df', u'order': None}], u'response_data': [], u'message': u'Yay working?', u'is_complete': False, u'custom_fields': [], u'subject': u'First test document'}}
        import pdb;pdb.set_trace()

    def signature_url(self):
        # Get the signature url
        signature_id = 'fd6d39525f3ef3da3069d038d3f9e1df'
        data = {
            'test_mode': 1,
            'client_id': CLIENT_ID,
        }
        req = HelloSign()
        req.url = "/embedded/sign_url/{signature_id}".format(signature_id=signature_id)
        resp = req.get(auth=AUTHENTICATION, headers={'accept': 'application/json'})

        import pdb;pdb.set_trace()