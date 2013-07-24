# -*- coding: UTF-8 -*-
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.utils.datastructures import SortedDict
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from bunch import Bunch

from glynt.apps.project.models import Project
from glynt.apps.project.services.ensure_project import PROJECT_CREATED

from glynt.apps.transact.views.intake import (FORMS as INTAKE_FORMS,)

TX_OPTIONS = {
    'INTAKE': {'forms': INTAKE_FORMS, 'templates': [], 'data_provider': Bunch({})},
    'CS': {'forms': [], 'templates': [], 'data_provider': Bunch({})},
    'SF': {'forms': [], 'templates': [], 'data_provider': Bunch({})},
    'ES': {'forms': [], 'templates': [], 'data_provider': Bunch({})},
}


class BuilderWizardView(NamedUrlSessionWizardView):
    """ Transaction Builder that compiles sets of form steps into a wizard """
    template_name = 'transact/forms/builder.html'
    form_list = []

    def get_update_url(self, **kwargs):
        return kwargs.get('context').get('form').get_update_url(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        If we have no forms defined then redirect to done
        """
        # setup the project
        self.project = get_object_or_404(Project, uuid=self.kwargs.get('project_uuid'))
        # Inject custom forms here as we need the request object
        self.custom_forms()
        if len(self.form_list) > 0:
            return super(BuilderWizardView, self).dispatch(request, *args, **kwargs)
        else:
            return self.done(form_list=[])

    def get_context_data(self, form, **kwargs):
        """ @BUSINESRULE set the page_title and page_description from the form class vars
        if they are present """
        context = super(BuilderWizardView, self).get_context_data(form, **kwargs)
        context.update({
            'page_title': context.get('form').page_title,
            'page_description': context.get('form').page_description,
            'update_url': self.get_update_url(context=context, project=self.project),
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
        """
        Dynamically build the form_list set based on the selected transactions
        """
        length_of_current_form_set = len(current_form_set.keys())
        for i, item in enumerate(form_set):
            # increment i + 1 as steps start at 1 not 0
            current_form_set[unicode(length_of_current_form_set + i + 1)] = item[1]  # return the form and not its name

        return current_form_set

    def get_step_url(self, step):
        return reverse(self.url_name, kwargs={'project_uuid': self.project.uuid, 'tx_range': self.kwargs.get('tx_range', ''), 'step': step})

    def get_form_kwargs(self, step=None):
        kwargs = super(BuilderWizardView, self).get_form_kwargs(step=step)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_form_initial(self, step):
        """
        Populate the form from our data_bag class
        """
        initial = super(BuilderWizardView, self).get_form_initial(step=step)

        data = self.form_list[step].get_data_bag(user=self.request.user)
        initial.update(data.get_data_bag())

        return initial

    def get_form_list(self):
        """
        Overridden to allow for sort()
        """
        form_list = super(BuilderWizardView, self).get_form_list()
        form_list.keyOrder.sort()
        return form_list

    def done(self, form_list, **kwargs):
        msg = _('Ok, You have created a new Project. Please read the instructions that follow.')
        messages.info(self.request, msg)

        PROJECT_CREATED.send(sender=self, instance=self.project, created=False)

        return HttpResponseRedirect(reverse('dashboard:overview'))
