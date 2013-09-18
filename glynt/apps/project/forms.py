# -*- coding: UTF-8 -*-
from django import forms
from django.core.urlresolvers import reverse

from parsley.decorators import parsleyfy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit

from public.forms import ContactForm

@parsleyfy
class ContactUsForm(ContactForm):
    """
    Form to handle contacting us when we don't offer the service required
    """

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'contact-us-form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('public:contact_us')

        self.helper.add_layout(Layout(
            Div(
                Field('name'),
                Field('message'),
                Field('email'),
                css_class='modal-body'
            ),
            Div(
                Submit('send', 'Send'),
                css_class='modal-footer'
            ),
        ))

        super(ContactUsForm, self).__init__(*args, **kwargs)


class CreateProjectForm(forms.Form):
    transaction_type = forms.CharField(widget=forms.HiddenInput)
