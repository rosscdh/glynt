# -*- coding: utf-8 -*-
from nose.tools import *
from mocktest import *

from glynt.apps.default.templatetags.glynt_helpers import colorize_acronym, moment_js


class TestTemplateTags(mocktest.TestCase):
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