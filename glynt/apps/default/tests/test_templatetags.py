# -*- coding: utf-8 -*-
from django import template
from django.utils import unittest
from django.test import TestCase
from django.test.utils import override_settings

from model_mommy import mommy

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin
from glynt.tests import TemplateRendererMixin

from django.contrib.auth.models import AnonymousUser

from glynt.apps.default.templatetags.glynt_helpers import (ABSOLUTE_STATIC_URL,
                                                           colorize_acronym,
                                                           pusher_js,
                                                           moment_js,
                                                           intercom_script,)


class TestTemplateTags(TestCase):
    fixtures = ['sites']

    def test_current_date_format(self):
        pass

    def test_current_site_domain(self):
        pass

    def test_document_status(self):
        pass

    def test_comment_form(self):
        pass

    @override_settings(SITE_ID=4)
    def test_ABSOLUTE_STATIC_URL(self):
        self.assertEqual(ABSOLUTE_STATIC_URL(), 'https://www.lawpal.com/static/')

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


class TestPusherJavascript(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    def setUp(self):
        super(TestPusherJavascript, self).setUp()
        self.client.login(username=self.lawyer_user.username, password=self.password)

    @override_settings(PROJECT_ENVIRONMENT='live')
    def test_pusher_js_production(self):
        css_selector = 'script#pusher-live-script'

        self.resp = self.client.get('/')
        c = self.pq(self.resp.content)
        css_object = c(css_selector)

        self.assertTrue(len(css_object) == 1)
        self.assertEqual('/static/js/pusher.2.1.2.min.js', css_object.attr['src'])

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_pusher_js_test(self):
        css_selector = 'script#pusher-test-env-mock-script'

        self.resp = self.client.get('/')
        c = self.pq(self.resp.content)
        css_object = c(css_selector)

        self.assertTrue(len(css_object) == 1)
        self.assertEqual('/static/js/angularjs/mocks/PusherMock.js', css_object.attr['src'])



class TestTemplateTag_ShowLoadingModal(unittest.TestCase):
    def setUp(self):
        pass


class TestTemplateTag_Intercom(unittest.TestCase):
    fixtures = ['test_cities']
    def setUp(self):

        self.user = mommy.make('auth.User')
        self.context = {
            'user': self.user
        }

        self.loggedout_user = AnonymousUser()
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
            , '{% intercom_script %}'
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


class TestHumaniseNumber(unittest.TestCase, TemplateRendererMixin):
    def setUp(self):
        self.expected_k_result = '500k'

        self.context = {
            'big_number': 500000,
            'no_strings_allowed' : 'lawpal rulez',
            'no_unicode_allowed' : u"\xc5",
            'no_empty_strings_allowed' : '',
            'no_neg_integers_allowed' : '-200000',
            'no_floating_allowed' : '200.403424230'
        }

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_humanise(self):
        result = self.render_template(
            '{% load glynt_helpers %}'
            , '{{ big_number|humanise_number }}'
            , context=self.context
        )

        self.assertEqual(result, self.expected_k_result)

    @override_settings(PROJECT_ENVIRONMENT='test')
    def test_humanise_converts_strings_to_zero(self):
        result = self.render_template(
            '{% load glynt_helpers %}'
            , '{{ no_strings_allowed|humanise_number }}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_unicode_to_zero(self):
        result = self.render_template(
            '{% load glynt_helpers %}'
            , '{{ no_unicode_allowed|humanise_number }}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_empty_string_to_zero(self):
        result = self.render_template(
            '{% load glynt_helpers %}'
            , '{{ no_empty_strings_allowed|humanise_number }}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_negative_integers_to_zero(self):
        result = self.render_template(
            '{% load glynt_helpers %}'
            , '{{ no_neg_integers_allowed|humanise_number }}'
            , context=self.context
        )

        self.assertEqual(result, '0')

    def test_humanise_converts_floating_to_zero(self):
        result = self.render_template(
            '{% load glynt_helpers %}'
            , '{{ no_floating_allowed|humanise_number }}'
            , context=self.context
        )

        self.assertEqual(result, '0')
