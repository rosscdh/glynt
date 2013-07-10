# -*- coding: UTF-8 -*-
from django.contrib.formtools.wizard.views import SessionWizardView
from django.utils.datastructures import SortedDict
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from glynt.apps.transact.views.intake import (FORMS as INTAKE_FORMS,)

TX_OPTIONS = {
    'INTAKE': {'forms': INTAKE_FORMS, 'templates': []},
    'CS': {'forms': [], 'templates': []},
    'SF': {'forms': [], 'templates': []},
    'ES': {'forms': [], 'templates': []},
}


class BuilderWizardView(SessionWizardView):
    """ Transaction Builder that compiles sets of form steps into a wizard """
    template_name = 'transact/forms/builder.html'
    form_list = []

    def dispatch(self, request, *args, **kwargs):
        # Inject custom forms here as we need the request object
        self.custom_forms()
        return super(BuilderWizardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        """ @BUSINESRULE set the page_title and page_description from the form class vars
        if they are present """
        context = super(BuilderWizardView, self).get_context_data(form, **kwargs)
        context.update({
            'page_title': context.get('form').page_title,
            'page_description': context.get('form').page_description
        })
        return context

    def custom_forms(self):
        """ custom method """
        self.form_list = SortedDict()  # reset the class var
        form_list = {}
        tx_range = self.kwargs.get('tx_range', '').split(',')
        if type(tx_range) == str:
            tx_range = [tx_range]

        # if intake is in the list, then it should be done first
        if 'INTAKE' in tx_range:
            tx_range.pop(tx_range.index('INTAKE'))  # remove the INTAKE item from the list
            self.add_form_to_set(current_form_set=form_list, form_set=TX_OPTIONS.get('INTAKE').get('forms'))

        # import the appropriate forms and their templates
        tx_options_keys = TX_OPTIONS.keys()
        for tx in tx_range:
            if tx in tx_options_keys:
                # @BUSINESSRULE - intake form must always be first
                self.add_form_to_set(current_form_set=form_list, form_set=TX_OPTIONS.get(tx).get('forms'))
        self.form_list = SortedDict(form_list)

    def add_form_to_set(self, current_form_set, form_set):
        length_of_current_form_set = len(current_form_set.keys())
        for i, item in enumerate(form_set):
            # increment i + 1 as steps start at 1 not 0
            current_form_set[unicode(length_of_current_form_set + i + 1)] = item[1]  # return the form and not its name

        return current_form_set

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:matching'))
