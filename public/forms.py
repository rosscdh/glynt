# -*- coding: utf-8 -*-
from django import forms

from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy


@parsleyfy
class ContactForm(BootstrapMixin, forms.Form):
    name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Name', 'tabindex':'1'}))
    message = forms.CharField(help_text="", widget=forms.Textarea(attrs={'placeholder':'Message', 'tabindex':'3'}))

    def inject_email(self):
        """ If the user is NOT signed in inject email """
        if not self.user.email:
            self.fields['email'] = forms.EmailField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Email', 'tabindex':'2'}))