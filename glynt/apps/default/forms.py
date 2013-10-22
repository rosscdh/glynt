# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django import forms

from parsley.decorators import parsleyfy


@parsleyfy
class ManualLoginForm(forms.Form):
    u = forms.CharField(label='Username/Email', required=True)
    p = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')

        super(ManualLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        user = authenticate(username=self.cleaned_data['u'],
                            password=self.cleaned_data['p'])

        if user is None:
            raise forms.ValidationError('Could not authenticate {user}'.format(user=self.cleaned_data['u']))
        else:
            login(self.request, user)