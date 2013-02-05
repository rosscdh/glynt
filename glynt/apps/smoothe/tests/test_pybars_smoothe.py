# -*- coding: utf-8 -*-
from nose.tools import *
from mocktest import *

from glynt.apps.smoothe.pybars_smoothe import Smoothe, DocChoiceException, DocSelectException


class TestTemplateToDoc(mocktest.TestCase):
    """ Class tests that the server-side handebars methods are called
    and retur the appropriate values """
    def setUp(self):
        self.subject = Smoothe()
        self.html_handlers = {
            # Doc Var
            'doc_var': u'{{#doc_var name="monkey"}}Bananarama{{/doc_var}}',
            # Doc Choice
            'doc_choice': u'{{#doc_choice name="animal_farm" choices="pig,horse,duck" is_static=true}}{{/doc_choice}}',
            'doc_choice_custom_not_is_static': u'{{#doc_choice name="animal_farm" choices="pig,horse,duck" is_static=false}}{{/doc_choice}}',
            'doc_choice_custom_unspecified_static': u'{{#doc_choice name="animal_farm" choices="pig,horse,duck"}}{{/doc_choice}}',
            # Doc Select
            'doc_select': u'{{#doc_select name="favourite_monkies" label="What are your favourite Monkies?"}}Gorillas{option}Baboons{option}Chimpanzies{option}Big Hairy Ones{{/doc_select}}',
            'doc_select_custom_join_by': u'{{#doc_select name="favourite_monkies" join_by="-A crazy night out with a Ham-" label="What are your favourite Monkies?"}}Gorillas{option}Baboons{option}Chimpanzies{option}Big Hairy Ones{{/doc_select}}',
            'doc_select_custom_subvariable': u'{{#doc_select name="favourite_monkies" label="What are your favourite Monkies?"}}Gorillas named {{#doc_var name="gorilla_name"}}{{/doc_var}}{option}Baboons{option}Chimpanzies named {{#doc_var name="chimp_name"}}{{/doc_var}}{option}Big Hairy Ones named {{#doc_var name="big_hairy_name"}}{{/doc_var}}{{/doc_select}}',
        }

    def testDocVar(self):
        self.subject.source_html = self.html_handlers['doc_var']
        context = {'monkey': u'This is some kind of Banana!'}
        self.subject.context = context

        assert self.subject.render(context) == u'This is some kind of Banana!'

    def testDocChoice(self):
        self.subject.source_html = self.html_handlers['doc_choice']
        context = {
            'animal_farm': u'pig'
        }
        self.subject.context = context
        assert self.subject.render(context) == u'pig'

    @raises(DocChoiceException)
    def testInvalidStaticDocChoice(self):
        self.subject.source_html = self.html_handlers['doc_choice']
        context = {
            'animal_farm': u'monkey'
        }
        self.subject.context = context
        self.subject.render(context)

    def testNotStaticDocChoice(self):
        self.subject.source_html = self.html_handlers['doc_choice_custom_not_is_static']
        context = {
            'animal_farm': u'gorilla'
        }
        self.subject.context = context
        assert self.subject.render(context) == u'gorilla'

    def testDefaultDocChoice(self):
        self.subject.source_html = self.html_handlers['doc_choice_custom_unspecified_static']
        context = {
            'animal_farm': u'gorilla'
        }
        self.subject.context = context
        assert self.subject.render(context) == u'gorilla'

    def testDocSelect(self):
        self.subject.source_html = self.html_handlers['doc_select']
        context = {
            'favourite_monkies': [u'Gorillas']
        }
        self.subject.context = context
        assert self.subject.render(context) == u'Gorillas'

    def testDocSelectMulti(self):
        """ When multi=true the method will return a string """
        self.subject.source_html = self.html_handlers['doc_select']
        context = {
            'favourite_monkies': [u'Gorillas', 'Big Hairy Ones']
        }
        self.subject.context = context
        # Joins on new line char
        assert self.subject.render(context) == u'Gorillas\rBig Hairy Ones'

    @raises(DocSelectException)
    def testDocSelectInvalidMulti(self):
        """ Elephants are NOT monkies """
        self.subject.source_html = self.html_handlers['doc_select']
        context = {
            'favourite_monkies': [u'Elephants', 'Gorillas']
        }
        self.subject.context = context
        self.subject.render(context)

    def testDocSelectCustomJoinBy(self):
        """ Join by '-A crazy night out with a Ham-' """
        self.subject.source_html = self.html_handlers['doc_select_custom_join_by']
        context = {
            'favourite_monkies': [u'Chimpanzies', 'Baboons']
        }
        self.subject.context = context
        eq_(self.subject.render(context), 'Chimpanzies-A crazy night out with a Ham-Baboons')

    def testDocSelectSubVariable(self):
        """ Test DocSelects that contain sub doc_vars """
        self.subject.source_html = self.html_handlers['doc_select_custom_subvariable']
        context = {
            'favourite_monkies': [u'Chimpanzies named George', 'Baboons'],
            'gorilla_name': 'Harald',
            'chimp_name': 'George',
            'big_hairy_name': 'Grumwald',
        }
        self.subject.context = context
        print self.subject.render(context)
        #eq_(self.subject.render(context), 'Chimpanzies-A crazy night out with a Ham-Baboons')


class TestHTMLExample(TestTemplateToDoc):
    def testGenericHTML(self):
        handlers = [v for k,v in self.html_handlers.items() if 'custom' not in k]
        html = '<html><head></head><body> <h1>A Test Title</h1> %s </body></html>'

        self.subject.source_html = html % ("<br/>".join(handlers),)
        context = {
            'monkey': u'Slurping Schwein on the Train from Moenchengladbach',
            'animal_farm': u'horse',
            'favourite_monkies': [u'Baboons', u'Gorillas']
        }
        self.subject.context = context

        html_result = self.subject.render(context)
        expected_html = html % ('Slurping Schwein on the Train from Moenchengladbach<br/>horse<br/>Baboons\rGorillas')

        eq_(html_result, expected_html)
