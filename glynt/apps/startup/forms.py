# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy
from models import Startup, Founder

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class StartupProfileSetupForm(BootstrapMixin, forms.Form):
    pass