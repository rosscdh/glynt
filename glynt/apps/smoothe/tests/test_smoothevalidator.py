# -*- coding: utf-8 -*-
from nose.tools import *
from mocktest import *

from glynt.apps.smoothe.services import SmootheValidateService

import logging
logger = logging.getLogger('django.test')


class TestSmootheValidator(mocktest.TestCase):
    def setUp(self):
        self.valid = [
            #('doc_var', '{{#doc_var name="principal_name"}} PRINCIPAL {{/doc_var}}')
            ('doc_select', '{{#doc_select name="test"}} A {option} B {{/doc_select}}')
        ]
        self.invalid = [
            ('doc_var', '{{#doc_var name="principal_name"}} PRINCIPAL') # expnd to include
            ,('doc_var', '{{#doc_var name="principal_name"}} PRINCIPAL {{/doc_select}}')
            ,('doc_choice', '{{#doc_choice name="principal_name"}} PRINCIPAL {{/doc_var}}')
            ,('doc_select', '{{#doc_select name="principal_name"}} PRINCIPAL {{/doc_choice}}')
        ]

        self.subject = SmootheValidateService

    def testValidSetup(self):
        for k,i in self.valid:
            s = self.subject(ident='valid-test', html=i)
            eq_(s.is_valid(), True)

    def testInvalidSetup(self):
        for k,i in self.invalid:
            s = self.subject(ident='invalid-test', html=i)
            eq_(s.is_valid(), False)
            eq_(len(s.errors), 1)
            eq_(s.error_msg, u"Unclosed tags: %s" % k)

    # def testInvalidDocSelect(self):
    #     invalid = [
    #         ('doc_select', '{{#doc_select name="principal_name"}} NO OPTION {{/doc_select}}')
    #     ]
    #     for k,i in invalid:
    #         s = self.subject(ident='invalid-test', html=i)
    #         eq_(s.is_valid(), False)
    #         eq_(len(s.errors), 1)
    #         eq_(s.error_msg, u"doc_select must contain at least 2 items seperated by \"{option}\", error at: name=\"principal_name\"")
