"""
Test the various graph services
"""

from django.test.utils import override_settings

import httpretty
import mocktest 
from glynt.apps.graph.services import LinkedinConnectionService
from oauth2 import Client


class LinkedinConnectionServiceTest(mocktest.TestCase):
    """ Test the linkedin Connections service
    used to acquire the linkedin users connections for populating the social graph"""
    def setUp(self):
        """
        """
        self.expected_url = 'http://api.linkedin.com/v1/people/~/connections?format=json'
        self.oauth_token = 'test_oauth_token'
        self.oauth_token_secret = 'test_oauth_token_secret'
        self.subject = LinkedinConnectionService(uid='123', oauth_token=self.oauth_token, oauth_token_secret=self.oauth_token_secret)


    def test_url(self):
        self.assertEqual(self.subject.get_url(), self.expected_url)

    def test_client_has_token(self):
        # we have a method called profile as part of LinkedinConnectionService
        self.subject.request()
        self.assertTrue('client' in self.subject.__dict__)
        self.assertTrue(self.subject.client is not None)
        self.assertTrue(isinstance(self.subject.client, Client))
        

    # @TODO: add the correct tests here
    @httpretty.activate
    def test_200_response(self):
        # note, that linkedin returns camelCasedAttrbiutes for json responses
        # we hack them to be more pythonic
        httpretty.register_uri(httpretty.GET, self.expected_url,
                               status=201,
                               body='{\n  "industry": "Internet",\n  "summary": "Summary here",\n  "currentStatus": "Monkies Rule",\n  "pictureUrl": "http://m3.licdn.com/mpr/mprx/0_G13Ym4CgyRCZ1zBI8AbDmUKpYsFZAnBIhqz3mU3DTM1ea-8wmzAthRviK-bbtlnFiri8Tp1jqBka"\n}')
        
        # response = self.subject.profile

        # self.assertTrue(response.keys() == ['status', 'industry', 'summary', 'photo_url'])

        # self.assertTrue(response.get('photo_url') == 'http://m3.licdn.com/mpr/mprx/0_G13Ym4CgyRCZ1zBI8AbDmUKpYsFZAnBIhqz3mU3DTM1ea-8wmzAthRviK-bbtlnFiri8Tp1jqBka')
        # self.assertTrue(response.get('industry') == 'Internet')
        # self.assertTrue(response.get('summary') == 'Summary here')
        # self.assertTrue(response.get('status') == 'Monkies Rule')
