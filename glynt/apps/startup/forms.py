# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy
from models import Startup, Founder

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class StartupProfileSetupForm(BootstrapMixin, forms.Form):
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))
    email = forms.EmailField(help_text="", widget=forms.TextInput(attrs={'data-trigger':'change','placeholder':'Email address', 'tabindex':'3'}))
    password = forms.CharField(label="Password", help_text="", widget=forms.PasswordInput(attrs={'placeholder':'Enter your password', 'data-trigger':'change', 'tabindex':'4'}))
    password_confirm = forms.CharField(label="", help_text="", widget=forms.PasswordInput(attrs={'placeholder':'Enter your password again', 'data-trigger':'change', 'minLength':'5', 'data-equalto':'#id_password', 'tabindex':'5'}))
    name = forms.CharField(label="Acme Inc", help_text="", widget=forms.TextInput(attrs={'placeholder':'Full Name', 'tabindex':'6'}))
    already_raised_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'7'}))
    process_raising_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'8'}))
    incubator_or_accelerator = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'class':'incubator', 'tabindex':'9'}))
    agree_tandc = forms.BooleanField(label='', widget=forms.CheckboxInput(attrs={'tabindex':'10'}))