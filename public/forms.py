# -*- coding: utf-8 -*-
from django import forms

from parsley.decorators import parsleyfy


@parsleyfy
class ContactForm(forms.Form):
    name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Name', 'tabindex':'1'}))
    message = forms.CharField(help_text="", widget=forms.Textarea(attrs={'placeholder':'Message', 'tabindex':'3'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.user = self.request.user

        super(ContactForm, self).__init__(*args, **kwargs)

        self.inject_email()
        self.set_initial()

    def set_initial(self):
        if self.user.is_authenticated():
            self.fields['name'].initial = self.user.get_full_name()
            self.fields['email'].initial = self.user.email

    def inject_email(self):
        """ If the user is NOT signed in OR they have no email address then show the email field """
        if not self.user.is_authenticated() or not self.user.email:
            self.fields['email'] = forms.EmailField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Email', 'tabindex':'2'}))
        else:
            self.fields['email'] = forms.EmailField(widget=forms.HiddenInput(), required=False)

    def clean_email(self):
        if self.cleaned_data['email']:
            email = self.cleaned_data['email']
        else:
            email = self.user.email
        return email