# -*- coding: UTF-8 -*-
from django.conf import settings

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from parsley.decorators import parsleyfy

from .models import ToDo
from django_filepicker.forms import FPUrlField


FILEPICKER_API_KEY = getattr(settings, 'FILEPICKER_API_KEY', None)
if FILEPICKER_API_KEY is None:
    raise Exception('You must specify a FILEPICKER_API_KEY in your local_settings.py')


class AttachmentForm(forms.Form):
    project = forms.IntegerField(widget=forms.HiddenInput)
    todo = forms.IntegerField(widget=forms.HiddenInput)
    attachment = FPUrlField(label='', help_text='', apikey=FILEPICKER_API_KEY,
                            additional_params={
                                'data-api-url': '/api/v1/todo/attachment',
                                'data-fp-button-text': 'Upload attachment',
                                'data-fp-button-class': 'btn btn-primary',
                                'data-fp-drag-class': 'drop-pane pull-right',
                                'data-fp-mimetypes': 'application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.ms-powerpoint, application/vnd.ms-excel',
                                'onchange': 'HandleAttachment(event)',
                            }
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                None,
                'project',
                'todo',
                'attachment',
            )
        )
        super(AttachmentForm, self).__init__(*args, **kwargs)


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo


@parsleyfy
class CutomerToDoForm(ToDoForm):
    """
    Form to allow user to create and edit ToDo items
    category is set via url param
    """
    project = forms.IntegerField(widget=forms.HiddenInput)

    class Meta(ToDoForm.Meta):
        exclude = ['user', 'slug', 'status', 'date_due', 'description', 'data']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.project_service = kwargs.pop('project_service')
        self.project_uuid = kwargs.pop('project_uuid')
        self.slug = kwargs.pop('slug')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('todo:edit', kwargs={'project_uuid': self.project_uuid, 'slug': self.slug})

        self.helper.layout = Layout(
            Fieldset(
                'General',
                'name',
                'category',
                'project',
            )
        )
        super(CutomerToDoForm, self).__init__(*args, **kwargs)

        self.fields['category'] = forms.ChoiceField(initial=self.request.GET.get('category', None), choices=self.project_service.category_initial())
        self.fields['project'].initial = self.project_service.project.pk

    def clean_project(self):
        return self.project_service.project
