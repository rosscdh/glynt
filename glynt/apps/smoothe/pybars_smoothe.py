# -*- coding: utf-8 -*-
from pybars import Compiler, strlist
import re


class DocChoiceException(Exception):
    def __init__(self, value, choices):
        self.value = value
        self.choices = choices
        message = u'The value provided "%s" is not one of [%s]' % (self.value, self.choices,)
        Exception.__init__(self, message)


class DocSelectException(DocChoiceException):
    pass


class Smoothe(object):
    source = None
    compiler = None
    template = None

    def __init__(self, context=None, source=None):
        self.compiler = Compiler()
        self.context = context
        self.source = source
        self.compiler.register_helper(u'doc_var', self.doc_var)
        self.compiler.register_helper(u'doc_choice', self.doc_choice)
        self.compiler.register_helper(u'doc_select', self.doc_select)
        self.compiler.register_helper(u'help_for', self.help_for)
        self.compiler.register_helper(u'doc_note', self.doc_note)

    def render(self, context):
        template = self.compiler.compile(self.source)
        if template:
            html = template(context)
            return unicode(''.join(html))
        return None

    def doc_var(self, this, *args, **kwargs):
        var_name = kwargs['name']
        if var_name in self.context:
            return self.context[var_name]
        return None

    def doc_choice(self, this, *args, **kwargs):
        var_name = kwargs['name']
        choices = kwargs['choices']
        is_static = kwargs['is_static'] if 'is_static' in kwargs else False

        if var_name in self.context:
            if self.context[var_name] in choices:
                return self.context[var_name]
            else:
                # Test for is static
                if is_static == False:
                    return self.context[var_name]
                else:
                    raise DocChoiceException(self.context[var_name], choices)
        return None

    def doc_select(self, this, *args, **kwargs):
        options = args[0]
        var_name = kwargs['name']
        choices_text = unicode(options['fn'](this))
        choices = [o.strip() for o in choices_text.split('{option}')]
        if var_name in self.context:
            selected_values = self.context[var_name]
            for o in selected_values:
                if o not in choices:
                    raise DocSelectException(self.context[var_name], choices)

            return "\r".join(self.context[var_name])
        return None

    def help_for(self, this, *args, **kwargs):
        """ No help is provided on the server side render of the doc """
        return None

    def doc_note(self, this, *args, **kwargs):
        """ No note is provided on the server side render of the doc """
        return None