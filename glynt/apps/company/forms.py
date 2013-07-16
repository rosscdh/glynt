# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from glynt.apps.utils import get_namedtuple_choices

COMPANY_STATUS_CHOICES = get_namedtuple_choices('COMPANY_STATUS_CHOICES', (
                            (1, 'pre_funding', 'Pre-funding'),
                            (2, 'have_term_sheet', 'Have term sheet'),
                            (3, 'currently_fund_raising', 'Currently fund raising'),
                            (4, 'already_funded', 'Already funded'),
                         ))


class CompanyProfileIsCompleteValidator(forms.Form):
    """ is used by the profile_complete template tag
    to evaluate the completeness of a companies profile """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    startup_name = forms.CharField(required=True)


class CompanyProfileForm(forms.Form):
    """
    The Company Setup Form
    """
    has_incubator = forms.BooleanField(label=_('We are part of an incubator'), initial=False)
    current_status = forms.ChoiceField(label=_('Current Status'), choices=COMPANY_STATUS_CHOICES.get_choices(), initial=COMPANY_STATUS_CHOICES.pre_funding, widget=forms.RadioSelect)
    profile_website = forms.URLField(label=_('Website or other profile'), widget=forms.TextInput(attrs={'data-type': 'url'}))
    description = forms.CharField(label=_('Short description of business'))
    has_option_plan = forms.BooleanField(label=_('Do you have a stock option plan?'), initial=False)
    target_states_and_countries = forms.CharField(label=_('States and countries where you will do business'))
    num_officers = forms.CharField(label=_('Initial number of directors and officers'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number'}))
    num_employees = forms.CharField(label=_('How many employees do you have?'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number'}))
    num_consultants = forms.CharField(label=_('How many consultants do you have?'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number'}))
    ip_nolonger_affiliated = forms.BooleanField(label=_('Is anyone involved in the creation of IP and no longer affiliated with the Company?'), initial=False)
    ip_otherthan_founder = forms.BooleanField(label=_('Is anyone other than the founders listed above involved in the creation of IP?'), initial=False)
    ip_university_affiliation = forms.BooleanField(label=_('Is anyone involved in the creation of IP affiliated with a university at the time?'), initial=False)
