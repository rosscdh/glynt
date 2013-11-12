# -*- coding: utf-8 -*-
"""
Contains useful mixins

# duplication below is due to the inability to inherit from classes with different base_classes
potential solution here
http://thomas.pelletier.im/2011/09/mixing-django-forms/

"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions


class ChangePasswordMixin(forms.Form):
    """ Mixin used to ensure passwords match """
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise exceptions.ValidationError(_('Passwords do not match'))

        return password


class ModelFormChangePasswordMixin(forms.ModelForm):
    """ MODEL FORM: Mixin used to ensure passwords match """
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'data-equalTo': '#id_confirm_password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'data-equalTo': '#id_password'}))

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise exceptions.ValidationError(_('Passwords do not match'))

        return password


class ConfirmChangePasswordMixin(forms.Form):
    """ Mixin used to ensure that the current_password was entered properly """
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)

    def clean_current_password(self):
        if not self.user:
            raise exceptions.ValidationError(_('No User was provided for this form'))

        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise exceptions.ValidationError(_('The Password entered for the "%s" field is not correct' % (self.fields['current_password'].label,)))

        return current_password


class ModelFormConfirmChangePasswordMixin(forms.ModelForm):
    """ MODEL FORM: Mixin used to ensure that the current_password was entered properly """
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)

    def clean_current_password(self):
        if not self.user:
            raise exceptions.ValidationError(_('No User was provided for this form'))

        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise exceptions.ValidationError(_('The Password entered for the "%s" field is not correct' % (self.fields['current_password'].label,)))

        return current_password


class ChangeUserDetailsMixin(object):
    """ Mixin used to change the users' details"""
    data = []
    user = None

    def update_user(self):
        fields_to_update = []

        if self.data.get('first_name', None) is not None:
            self.user.first_name = self.data.get('first_name')
            fields_to_update.append('first_name')

        if self.data.get('last_name', None) is not None:
            self.user.last_name = self.data.get('last_name')
            fields_to_update.append('last_name')

        if self.data.get('email', None) is not None:
            self.user.email = self.data.get('email')
            fields_to_update.append('email')

        # update the user only if changes happened
        if len(fields_to_update) > 0:
            self.user.save(update_fields=fields_to_update)
