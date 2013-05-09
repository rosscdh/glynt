# -*- coding: utf-8 -*-
from django import template
from django.test import LiveServerTestCase
from django.utils import unittest
from django.test.utils import override_settings
from nose.tools import *

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


class TestTemplateTag_Intercom(unittest.TestCase):
    fixtures = ['test_cities']
    def setUp(self):

        self.user = UserFactory.create()
        self.context = {
            'user': self.user
        }

        self.loggedout_user = LoggedOutUserFactory.create()
        self.loggedout_context = {
            'user': self.loggedout_user
        }

    def render_template(self, *args, **kwargs):
        context = kwargs.get('context', {})
        t = template.Template(''.join(args))
        c = template.Context(context)
        return t.render(c)

    @override_settings(PROJECT_ENVIRONMENT='dev')
    def test_does_not_show_in_dev_for_both_user_states(self):
        # Not Logged in
        result = intercom_script(self.loggedout_context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is None)
        self.assertTrue(result.get('show_widget') is False)
        # Logged in
        result = intercom_script(self.context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is None)
        self.assertTrue(result.get('show_widget') is False)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_not_authenticated_shows_but_no_hash(self):
        self.assertFalse(self.loggedout_user.is_authenticated())

        result = intercom_script(self.loggedout_context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is None)
        self.assertTrue(result.get('show_widget') is False)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_is_authenticated_and_shows_hash(self):
        self.assertTrue(self.user.is_authenticated())

        result = intercom_script(self.context)
        self.assertTrue('intercomio_userhash' in result)
        self.assertTrue(result.get('intercomio_userhash') is not None)
        self.assertTrue(result.get('show_widget') is True)


    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_presence(self):
        intercom_result = intercom_script(self.context)
        result = self.render_template(
            '{% load glynt_helpers %}'
            ,'{% intercom_script %}'
            , context=self.context
        )

        self.assertTrue(intercom_result.get('show_widget') is True)
        assert 'user_hash:' in result
        assert 'user_id:' in result
        assert 'name:' in result
        assert 'email:' in result

        assert 'user_id: "%s"' % intercom_result.get('user').pk in result
        assert 'name: "%s"' % intercom_result.get('user').get_full_name() in result
        assert 'email: "%s"' % intercom_result.get('user').email in result
        assert 'user_hash: "%s"' % intercom_result.get('intercomio_userhash') in result