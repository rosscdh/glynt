# -*- coding: UTF-8 -*-
from django import forms


class CreateProjectForm(forms.Form):
    transaction_type = forms.CharField(widget=forms.HiddenInput)
