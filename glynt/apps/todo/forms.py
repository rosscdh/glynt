# -*- coding: UTF-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from .models import ToDo


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo


class CutomerToDoForm(ToDoForm):
    class Meta(ToDoForm.Meta):
        exclude = ['project', 'user', 'slug', 'status', 'description', 'data']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'General',
                'name',
                'date_due',
            ),
            Fieldset(
                'Info',
                'category',
                'description',
            ),
            ButtonHolder(
                Submit('submit', 'Change', css_class='')
            )
        )
        super(CutomerToDoForm, self).__init__(*args, **kwargs)