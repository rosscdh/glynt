# -*- coding: utf-8 -*-
from django.conf import settings
from nose.tools import *
from mocktest import *

from glynt.apps.export.utils import UnsupportedMediaPathException, fetch_resources


class TestFetchResources(mocktest.TestCase):
    def test_fetch_resources(self):
        result = fetch_resources(uri='%smonkey.png'%(settings.STATIC_URL,))
        assert settings.STATIC_ROOT in result

        result = fetch_resources(uri='%smonkey.png'%(settings.MEDIA_URL,))
        assert settings.MEDIA_ROOT in result


    @raises(UnsupportedMediaPathException)
    def test_fetch_resources_unsupported(self):
        result = fetch_resources(uri='/totally_wrong/monkey.png')