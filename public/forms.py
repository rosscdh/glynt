# -*- coding: utf-8 -*-
from django import forms

from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy


@parsleyfy
class ContactForm(BootstrapMixin, forms.Form):
    name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Name', 'tabindex':'1'}))
    message = forms.CharField(help_text="", widget=forms.Textarea(attrs={'placeholder':'Message', 'tabindex':'3'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.user = self.request.user
        super(ContactForm, self).__init__(*args, **kwargs)
        self.inject_email()

    def inject_email(self):
        """ If the user is NOT signed in OR they have no email address then show the email field """
        if not self.user.is_authenticated() or not self.user.email:
            self.fields['email'] = forms.EmailField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Email', 'tabindex':'2'}))