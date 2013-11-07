# -*- coding: utf-8 -*-
from django import forms

from parsley.decorators import parsleyfy

from models import Signature


@parsleyfy
class SignatureForm(forms.ModelForm):
    user = None
    subject = forms.CharField(required=True)
    message =  forms.CharField(required=True)

    class Meta:
        model = Signature
        exclude = ('data',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SignatureForm, self).__init__(*args, **kwargs)

    def signatories(self):
        return [('ross', 'ross@lawpal.com'),]

    def documents(self):
        return []