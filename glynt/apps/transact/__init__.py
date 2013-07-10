# coding: utf-8
import os
from django import forms

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

FLYFORM_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/flyforms/')
TRANSACTION_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/transactions/')


class BuilderBaseForm(forms.Form):
    """ provide accessors for the page meta properties
    that need to be defined in the form to allow us to modify the templates
    based on the form being viewed """
    @property
    def page_title(self):
        return getattr(self.__class__, 'page_title', None)

    @property
    def page_description(self):
        return getattr(self.__class__, 'page_description', None)
