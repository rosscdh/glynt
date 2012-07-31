# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _


class BaseFlyForm(forms):
	""" This form is the basis for the self generating form representations
	it requires that a valid json_object be passed in which adheres to the following schema
	"""
	def __init__(self, json_form_representation, *args, **kwargs):
		super(BaseFlyForm, self).__init__(*args, **kwargs)
