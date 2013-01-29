# -*- coding: utf-8 -*-
from nose.tools import *
from mocktest import *

from glynt.apps.smoothe.pybars_smoothe import Smoothe, DocChoiceException, DocSelectException


class TestTemplateToDoc(mocktest.TestCase):
    """ Class tests that the server-side handebars methods are called
    and retur the appropriate values """
    def setUp(self):
        self.subject = Smoothe()
        self.html = {
            # Doc Var
            'doc_var': u'{{#doc_var name="monkey"}}Bananarama{{/doc_var}}',
            # Doc Choice
            'doc_choice': u'{{#doc_choice name="animal_farm" choices="pig,horse,duck" is_static=true}}{{/doc_choice}}',
            'doc_choice_not_is_static': u'{{#doc_choice name="animal_farm" choices="pig,horse,duck" is_static=false}}{{/doc_choice}}',
            'doc_choice_unspecified_static': u'{{#doc_choice name="animal_farm" choices="pig,horse,duck"}}{{/doc_choice}}',
            # Doc Select
            'doc_select': u'{{#doc_select name="favourite_monkies" label="What are your favourite Monkies?"}}Gorillas{option}Baboons{option}Chimpanzies{option}Big Hairy Ones{{/doc_select}}',
        }

    def testDocVar(self):
        self.subject.source = self.html['doc_var']
        context = {'monkey': u'This is some kind of Banana!'}
        self.subject.context = context

        assert self.subject.render(context) == u'This is some kind of Banana!'

    def testDocChoice(self):
        self.subject.source = self.html['doc_choice']
        context = {
            'animal_farm': u'pig'
        }
        self.subject.context = context
        assert self.subject.render(context) == u'pig'

    @raises(DocChoiceException)
    def testInvalidStaticDocChoice(self):
        self.subject.source = self.html['doc_choice']
        context = {
            'animal_farm': u'monkey'
        }
        self.subject.context = context
        self.subject.render(context)

    def testNotStaticDocChoice(self):
        self.subject.source = self.html['doc_choice_not_is_static']
        context = {
            'animal_farm': u'gorilla'
        }
        self.subject.context = context
        assert self.subject.render(context) == u'gorilla'

    def testDefaultDocChoice(self):
        self.subject.source = self.html['doc_choice_unspecified_static']
        context = {
            'animal_farm': u'gorilla'
        }
        self.subject.context = context
        assert self.subject.render(context) == u'gorilla'

    def testDocSelect(self):
        self.subject.source = self.html['doc_select']
        context = {
            'favourite_monkies': [u'Gorillas']
        }
        self.subject.context = context
        assert self.subject.render(context) == u'Gorillas'

    def testMultiDocSelect(self):
        """ When multi=true the method will return a string """
        self.subject.source = self.html['doc_select']
        context = {
            'favourite_monkies': [u'Gorillas', 'Big Hairy Ones']
        }
        self.subject.context = context
        # Joins on new line char
        assert self.subject.render(context) == u'Gorillas\rBig Hairy Ones'

    @raises(DocSelectException)
    def testInvalidMultiDocSelect(self):
        """ Elephants are NOT monkies """
        self.subject.source = self.html['doc_select']
        context = {
            'favourite_monkies': [u'Elephants', 'Gorillas']
        }
        self.subject.context = context
        self.subject.render(context)
