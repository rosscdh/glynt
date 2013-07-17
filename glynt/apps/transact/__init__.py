# coding: utf-8
import os
from django import forms
from crispy_forms.helper import FormHelper

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

FLYFORM_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/flyforms/')
TRANSACTION_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/transactions/')


def import_module_class(name):
    components = name.split('.')
    module_path = components[:-1]
    klass = components[-1:]
    mod = __import__('.'.join(module_path), fromlist=klass) # import the class and module
    klass = getattr(mod, klass[0])
    return klass


class BuilderBaseForm(forms.Form):
    """ provide accessors for the page meta properties
    that need to be defined in the form to allow us to modify the templates
    based on the form being viewed """
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()
        # remove the double form creation
        self.helper.form_tag = kwargs.get('use_crispy_form_tag', False)

        self.request = kwargs.pop('request', None)
        self.user = self.request.user if self.request and hasattr(self.request, 'user') else None

        super(BuilderBaseForm, self).__init__(*args, **kwargs)

    @property
    def data_bag(self):
        return getattr(self.__class__, 'data_bag', None)

    @property
    def page_title(self):
        return getattr(self.__class__, 'page_title', None)

    @property
    def page_description(self):
        return getattr(self.__class__, 'page_description', None)

    @classmethod
    def get_data_bag(self, **kwargs):
        data_bag_klass = import_module_class(self.data_bag)
        return data_bag_klass(**kwargs)

    # def is_valid(self, *args, **kwargs):
    #     """
    #     Call our custom save method
    #     this is not really great as calling save is assumed here, which is not natural behaviour
    #     is_valid should only return if its valid or not. Need to find a better way
    #     """
    #     is_valid = super(BuilderBaseForm, self).is_valid(*args, **kwargs)
    #     if is_valid:
    #         self.save()
    #     return is_valid


    def save(self, *args, **kwargs):
        data_bag = self.get_data_bag(user=self.user)
        return data_bag.save(**self.cleaned_data)