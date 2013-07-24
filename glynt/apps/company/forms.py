# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from glynt.apps.transact import BuilderBaseForm
from glynt.apps.company import COMPANY_STATUS_CHOICES
from glynt.apps.company import OPTION_PLAN_STATUS_CHOICES


class CompanyProfileForm(BuilderBaseForm):
    """
    The Company Setup Form
    """
    founder_name = forms.CharField()
    founder_email = forms.EmailField()

    incubator = forms.CharField(label=_('Incubator or accelerator'), required=False, help_text="If you are currently particpating in an accelerator please enter it here.")
    current_status = forms.ChoiceField(label=_('Current funding status'), choices=COMPANY_STATUS_CHOICES.get_choices(), initial=COMPANY_STATUS_CHOICES.pre_funding, widget=forms.RadioSelect)
    profile_website = forms.URLField(label=_('Website or other profile'), help_text="", widget=forms.TextInput(attrs={'data-type': 'url', 'placeholder': 'http://angel.co/lawpal'}))
    description = forms.CharField(label=_('Short description of startup'), required=False, help_text="Skip this if you have entered a website or AngelList profile")
    option_plan_status = forms.ChoiceField(label=_('Option plan'), choices=OPTION_PLAN_STATUS_CHOICES.get_choices(), initial=OPTION_PLAN_STATUS_CHOICES.would_like, widget=forms.RadioSelect)

    target_states_and_countries = forms.CharField(label=_('Where will you do business?'), initial="California", help_text="e.g. California, New York. Separate with a comma.", widget=forms.TextInput(attrs={'placeholder': 'California'}))
    num_officers = forms.CharField(label=_('Number of Directors and Officers'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_employees = forms.CharField(label=_('Number of employees'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_consultants = forms.CharField(label=_('Number of consultants'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_option_holders = forms.CharField(label=_('Number of option holders'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    ip_nolonger_affiliated = forms.BooleanField(label=_('Someone involved in the creation of IP is no longer affiliated with the Company'), required=False, initial=False)
    ip_otherthan_founder = forms.BooleanField(label=_('Someone other than the founders listed was involved in the creation of IP'), required=False, initial=False)
    ip_university_affiliation = forms.BooleanField(label=_('Someone involved in the creation of IP was affiliated with a university at the time'), required=False, initial=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Founding Team',
                'founder_email',
                'founder_name',
                **{'data-region-clone': 'true', 'data-region-name': 'founders', 'class': 'founder-block'}
            ),
            Fieldset(
                'About your Startup',
                'incubator',
                'current_status',
                'profile_website',
                'description',
                'target_states_and_countries',
                'num_officers',
                'num_employees',
                'num_consultants',
                'option_plan_status',
                'num_option_holders',
                'ip_nolonger_affiliated',
                'ip_otherthan_founder',
                'ip_university_affiliation',
            )
        )
        super(CompanyProfileForm, self).__init__(*args, **kwargs)