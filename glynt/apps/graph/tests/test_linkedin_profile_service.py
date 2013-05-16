"""
Test the various graph services
"""

from django.test.utils import override_settings

import httpretty
import mocktest

from glynt.apps.graph.services import LinkedinProfileService


class LinkedinProfileServiceTest(mocktest.TestCase):
    """ Test the linkedin Profile services
    used to acquire the linkedin users profile information and photo"""
    @override_settings(LINKEDIN_CONSUMER_KEY='key', LINKEDIN_CONSUMER_SECRET='secret')
    def setUp(self):
        """
        """
        self.expected_url = 'http://api.linkedin.com/v1/people/123:(picture-url,current-status,industry,summary)?format=json'
        self.oauth_token = 'test_oauth_token'
        self.oauth_token_secret = 'test_oauth_token_secret'
        self.subject = LinkedinProfileService(uid='123', oauth_token=self.oauth_token, oauth_token_secret=self.oauth_token_secret)

    def test_url(self):
        self.assertEqual(self.subject.get_url(), self.expected_url)

    def test_profile_is_present(self):
        # we have a method called profile as part of LinkedinProfileService
        self.assertTrue('profile' in dir(self.subject))

    @httpretty.activate
    def test_200_response(self):
        # note, that linkedin returns camelCasedAttrbiutes for json responses
        # we hack them to be more pythonic
        httpretty.register_uri(httpretty.GET, self.expected_url,
                               status=201,
                               body='{\n  "industry": "Internet",\n  "summary": "Summary here",\n  "currentStatus": "Monkies Rule",\n  "pictureUrl": "http://m3.licdn.com/mpr/mprx/0_G13Ym4CgyRCZ1zBI8AbDmUKpYsFZAnBIhqz3mU3DTM1ea-8wmzAthRviK-bbtlnFiri8Tp1jqBka"\n}')
        
        response = self.subject.profile

        self.assertTrue(response.keys() == ['status', 'industry', 'summary', 'photo_url'])

        self.assertTrue(response.get('photo_url') == 'http://m3.licdn.com/mpr/mprx/0_G13Ym4CgyRCZ1zBI8AbDmUKpYsFZAnBIhqz3mU3DTM1ea-8wmzAthRviK-bbtlnFiri8Tp1jqBka')
        self.assertTrue(response.get('industry') == 'Internet')
        self.assertTrue(response.get('summary') == 'Summary here')
        self.assertTrue(response.get('status') == 'Monkies Rule')

    @httpretty.activate
    def test_200_partial_response(self):
        """ if the user has not provided a photo or status or summary at linked in
        then we need to cater to that """
        # note, that linkedin returns camelCasedAttrbiutes for json responses
        # we hack them to be more pythonic
        httpretty.register_uri(httpretty.GET, self.expected_url,
                               status=201,
                               body='{\n  "industry": "Internet"}')
        
        response = self.subject.profile

        self.assertTrue(response.keys() == ['status', 'industry', 'summary', 'photo_url'])

        self.assertTrue(response.get('photo_url') is None)
        self.assertTrue(response.get('industry') == 'Internet')
        self.assertTrue(response.get('summary')  is None)
        self.assertTrue(response.get('status')  is None)

    @httpretty.activate
    def test_mangled_response(self):
        """ if the user has not provided a photo or status or summary at linked in
        then we need to cater to that """
        # note, that linkedin returns camelCasedAttrbiutes for json responses
        # we hack them to be more pythonic
        httpretty.register_uri(httpretty.GET, self.expected_url,
                               status=201,
                               body="{\n  'industry': ')") # note the mangeld json
        
        response = self.subject.profile

        self.assertTrue(response.keys() == ['status', 'industry', 'summary', 'photo_url'])

        self.assertTrue(response.get('photo_url') is None)
        self.assertTrue(response.get('industry') is None)
        self.assertTrue(response.get('summary')  is None)
        self.assertTrue(response.get('status')  is None)
