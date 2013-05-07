# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.utils import unittest
from django.test.client import Client
from django.test.utils import override_settings
from nose.tools import *

from BeautifulSoup import BeautifulSoup

from glynt.apps.factories import UserFactory, LoggedOutUserFactory

from glynt.apps.default.templatetags.glynt_helpers import colorize_acronym,  \
        moment_js, intercom_script


class TestTemplateTags(unittest.TestCase):
    def test_current_date_format(self):
        pass
    def test_current_site_domain(self):
        pass
    def test_document_status(self):
        pass
    def test_comment_form(self):
        pass
    def test_colorize_acronym(self):
        assert colorize_acronym('monkey') == 'c5'
        assert colorize_acronym('cl') == 'c1'
        assert colorize_acronym('la') == 'c2'
        assert colorize_acronym('nda') == 'c3'
        assert colorize_acronym('hsp') == 'c4'

    def test_moment_js(self):
        result = moment_js()
        assert result.get('selector') == '[data-humanize-date]'

        result = moment_js('#monkey')
        assert result.get('selector') == '#monkey'


class TestTemplateTag_ShowLoadingModal(unittest.TestCase):
    def setUp(self):
        pass


class TestTemplateTag_Intercom(LiveServerTestCase):
    fixtures = ['test_cities']
    def setUp(self):
        self.client = Client()

        self.user = UserFactory.create()
        self.context = {
            'user': self.user
        }

        self.loggedout_user = LoggedOutUserFactory.create()
        self.loggedout_context = {
            'user': self.loggedout_user
        }

    def get_intercom_tag(self, result):
        soup = BeautifulSoup(result.content)
        return soup.findAll('script', id="IntercomSettingsScriptTag")

    @override_settings(PROJECT_ENVIRONMENT='dev')
    def test_does_not_show_in_dev_for_both_user_states(self):
        # Not Logged in
        result = intercom_script(self.loggedout_context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is None)
        # Logged in
        result = intercom_script(self.context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is None)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_not_authenticated_shows_but_no_hash(self):
        self.assertFalse(self.loggedout_user.is_authenticated())

        result = intercom_script(self.loggedout_context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is None)


    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_is_authenticated_and_shows_hash(self):
        self.assertTrue(self.user.is_authenticated())

        result = intercom_script(self.context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is not None)


    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_presence(self):
        result = self.client.get('/')
        script_tag = self.get_intercom_tag(result)

        self.assertTrue(len(script_tag) == 1) # we have 1 script of this id
