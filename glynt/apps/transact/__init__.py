# coding: utf-8
import os
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

FLYFORM_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/flyforms/')
TRANSACTION_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/transactions/')


def import_module_class(name):
    try:
        components = name.split('.')
        module_path = components[:-1]
        klass = components[-1:]
        mod = __import__('.'.join(module_path), fromlist=klass)  # import the class and module
        klass = getattr(mod, klass[0])
    except AttributeError:
        klass = None
    return klass


class BuilderBaseForm(forms.Form):
    """ provide accessors for the page meta properties
    that need to be defined in the form to allow us to modify the templates
    based on the form being viewed """
    page_title = None
    page_description = None
    data_bag = None

    #  stores the JSON data used to handle repeatables etc
    form_json_data = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()

        if hasattr(self.helper, 'layout'):
            self.helper[:-1].wrap(Field, 'form_json_data')

        # remove the double form creation
        self.helper.form_tag = kwargs.get('use_crispy_form_tag', False)

        self.request = kwargs.pop('request', None)
        self.user = self.request.user if self.request and hasattr(self.request, 'user') else None

        super(BuilderBaseForm, self).__init__(*args, **kwargs)

        self.initial_form_json_data(**kwargs)

    def initial_form_json_data(self, **kwargs):
        """ Populate the form_json_data field """
        if self.data_bag is not None:
            self.fields['form_json_data'].initial = self.get_data_bag(user=self.user, **kwargs.get('initial', {})).as_json()

    @classmethod
    def get_data_bag(self, **kwargs):
        data_bag_klass = import_module_class(self.data_bag)
        if data_bag_klass is not None:
            return data_bag_klass(**kwargs)
        else:
            return None

    def is_valid(self, *args, **kwargs):
        """
        Call our custom save method
        this is not really great as calling save is assumed here, which is not natural behaviour
        is_valid should only return if its valid or not. Need to find a better way
        """
        is_valid = super(BuilderBaseForm, self).is_valid(*args, **kwargs)
        if is_valid:
            self.save()
        return is_valid

    def save(self, *args, **kwargs):
        data_bag = self.get_data_bag(user=self.user)
        if data_bag and hasattr(data_bag, 'save'):

            # remove the unrequired fields
            self.cleaned_data.pop('form_json_data')

            return data_bag.save(**self.cleaned_data)
