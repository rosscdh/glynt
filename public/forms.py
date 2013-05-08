# -*- coding: utf-8 -*-
from django import forms

from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy


@parsleyfy
class ContactForm(BootstrapMixin, forms.Form):
    name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Name', 'tabindex':'1'}))
    email = forms.EmailField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Email', 'tabindex':'2'}))
    message = forms.CharField(help_text="", widget=forms.Textarea(attrs={'placeholder':'Message', 'tabindex':'3'}))

    def clean_email(self):
        # TODO Need to check is user is logged in and if so fill in their email
        data = self.cleaned_data['email']
        return data