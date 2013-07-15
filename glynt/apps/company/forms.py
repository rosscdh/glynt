# -*- coding: UTF-8 -*-
from django import forms


class CompanyProfileIsCompleteValidator(forms.Form):
    """ is used by the profile_complete template tag
    to evaluate the completeness of a companies profile """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    startup_name = forms.CharField(required=True)
