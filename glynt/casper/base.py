# -*- coding: utf-8 -*-
from django.conf import settings
from casper.tests import CasperTestCase
import os.path


class BaseCasperJs(CasperTestCase):
    """
    Base Class with helper methods to load casper tests
    """
    def load_casper_file(self, js_file, **kwargs):
        casper_test_folder_path = kwargs.get('casper_test_folder', 'casper-tests')
        # test_path must be defined on inheriting class
        # test_path = os.path.dirname(__file__)
        test_path = getattr(self, 'test_path', os.path.dirname(__file__))

        test_path = os.path.join(test_path, 
                                 casper_test_folder_path,
                                 js_file
                                )
        print test_path
        kwargs.update({
            'casper_helper_js_path': kwargs.get('casper_helper_js_path', os.path.join(settings.SITE_ROOT, 'glynt/casper/jslib/djangocasper.js'))
        })

        return self.casper(test_path, **kwargs)