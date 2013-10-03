# -*- coding: UTF-8 -*-
import os
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset

import json
import logging
logger = logging.getLogger('django.request')

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

FLYFORM_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/flyforms/')
TRANSACTION_TEMPLATE_PATH = os.path.join(MODULE_PATH, 'templates/transactions/')


def import_module_class(name):
    """
    func used to import the bunch classes which load
    the .yml files
    """
    try:
        components = name.split('.')
        module_path = components[:-1]
        klass = components[-1:]
        mod = __import__('.'.join(module_path), fromlist=klass)  # import the class and module
        klass = getattr(mod, klass[0])
    except AttributeError:
        klass = None
    return klass


class CrispyExFieldsetFieldRemovalMixin(object):
    """
    Mixin that will remove any field not in the
    Crispy fieldset Definitions
    """
    def unify_fields(self, *args, **kwargs):
        """
        Remove fields that are not specified in the
        crispy fieldset
        """
        specified_fields = []
        form_fields = set(self.fields.copy())

        if hasattr(self, 'helper'):
            if hasattr(self.helper, 'layout'):

                for positions, field_name in self.helper.layout.get_field_names():
                    #logger.debug('Field: {f}'.format(f=field_name))
                    specified_fields.append(field_name)

                specified_fields = set(specified_fields)  # convert to a set

                for f in form_fields:
                    if f not in specified_fields:
                        del self.fields[f]


class BuilderBaseForm(forms.Form):
    """ provide accessors for the page meta properties
    that need to be defined in the form to allow us to modify the templates
    based on the form being viewed """
    page_title = None
    page_description = None
    data_bag = None

    #  stores the JSON data used to handle repeatables etc
    form_json_data = forms.CharField(required=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'helper'):
            self.helper = FormHelper()

        if hasattr(self.helper, 'layout'):
            # create a default fieldset with no label and contains our hidden
            # form_json_data field
            form_json_data_fieldset = Fieldset(None, 'form_json_data')
            self.helper.layout.fields.insert(0, form_json_data_fieldset)

        # remove the double form creation
        self.helper.form_tag = kwargs.get('use_crispy_form_tag', False)

        self.request = kwargs.pop('request', None)
        self.user = self.request.user if self.request and hasattr(self.request, 'user') else None

        super(BuilderBaseForm, self).__init__(*args, **kwargs)

        self.initial_form_json_data(**kwargs)

    @classmethod
    def get_data_bag(self, **kwargs):
        data_bag_klass = import_module_class(self.data_bag)
        if data_bag_klass is not None:
            return data_bag_klass(**kwargs)
        else:
            return None

    def initial_form_json_data(self, **kwargs):
        """
        Populate the form_json_data field
        """
        if self.data_bag is not None:
            self.fields['form_json_data'].initial = self.get_data_bag(instance=self.request.project, request=self.request, user=self.user, **kwargs.get('initial', {})).as_json()

    def save_data_bag(self, cleaned_data, **kwargs):
        """
        Custom save method called by builder.py when saving our the completed
        is_valid form
        """
        data_bag = self.get_data_bag(instance=self.request.project, request=self.request, user=self.user, **kwargs)

        form_json_data = json.loads(cleaned_data.pop('form_json_data', '{}'))

        if data_bag is None:
            return None
        else:
            if data_bag._model_databag_field:
                if form_json_data is not None:
                    data_bag.save(**form_json_data)

        return form_json_data
