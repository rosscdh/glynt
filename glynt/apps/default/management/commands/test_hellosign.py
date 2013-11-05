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
        api = HelloSign()
        account_info = api.account.get(auth=AUTHENTICATION)
        print account_info
        
        # Authorize Url # https://www.hellosign.com/oauth/authorize?response_type=code&client_id=9bc892af173754698e3fa30dedee3826&state=02a263f8
        #resp = requests.get('https://api.hellosign.com/oauth/authorize', params={'response_type': 'code', 'client_id': '9bc892af173754698e3fa30dedee3826', 'state': '02a263f8'})

        # Craete embedded
        data = {
            'test_mode': 1,
            'client_id': CLIENT_ID,
            'subject': 'First test document',
            'message': 'Yay working?',
            'signers[0][name]': 'Ross C',
            'signers[0][email_address]': 'ross@lawpal.com',
        }
        files = {
            'file[0]': open('/Users/rosscdh/Projects/lawpal/glynt/glynt/casper/test.pdf')
        }
        #resp = requests.post('https://api.hellosign.com/v3/signature_request/create_embedded', auth=AUTHENTICATION, data=data, files=files)
        resp = HelloSign().signature_request.create_embedded.post(auth=AUTHENTICATION, data=data, files=files)
        print resp.json()

        import pdb;pdb.set_trace()