# -*- coding: UTF-8 -*-
from django.conf import settings

from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from parsley.decorators import parsleyfy
from django_filepicker.forms import FPUrlField

from glynt.apps.utils import generate_unique_slug

from .models import ToDo

import logging
logger = logging.getLogger('django.request')

FILEPICKER_API_KEY = getattr(settings, 'FILEPICKER_API_KEY', None)
if FILEPICKER_API_KEY is None:
    raise Exception('You must specify a FILEPICKER_API_KEY in your local_settings.py')


@parsleyfy
class FeedbackRequestForm(forms.Form):
    #comment = forms.CharField(widget=forms.Textarea)
    comment = forms.CharField(required=False, label="Optional Comment", widget=forms.Textarea(attrs={'placeholder': 'Enter an optional comment here...', 'data-rangelength': '[0,1024]', 'rows': '2'}))


class AttachmentForm(forms.Form):
    project = forms.IntegerField(widget=forms.HiddenInput)
    todo = forms.IntegerField(widget=forms.HiddenInput)
    attachment = FPUrlField(label='',
                            help_text='',
                            apikey=FILEPICKER_API_KEY,
                            additional_params={
                                'data-api-url': '/api/v1/attachment',
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
class CustomerToDoForm(ToDoForm):
    """
    Form to allow user to create and edit ToDo items
    category is set via url param
    """
    project = forms.IntegerField(widget=forms.HiddenInput)

    class Meta(ToDoForm.Meta):
        exclude = ['user', 'slug', 'status', 'date_due', 'description', 'data', 'sort_position', 'sort_position_by_cat', 'item_hash_num']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.project_service = kwargs.pop('project_service')
        self.project_uuid = kwargs.pop('project_uuid')
        self.slug = kwargs.pop('slug')
        self.is_create = kwargs.pop('is_create', False)

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

        super(CustomerToDoForm, self).__init__(*args, **kwargs)

        if self.is_create or self.request.POST.get('category', None) is not None:
            self.fields['category'] = forms.ChoiceField(initial=self.request.GET.get('category', self.request.POST.get('category', self.instance.category)), choices=self.project_service.category_initial())
        else:
            del self.fields['category']
            self._meta.exclude += ['category']

        self.fields['project'].initial = self.project_service.project.pk


    def clean_project(self):
        return self.project_service.project

    def save(self, *args, **kwargs):
        """ Ensure that we have a slug, required for creating new items manually """
        obj = super(CustomerToDoForm, self).save(*args, **kwargs)

        if obj.slug in [None, '']:
            obj.slug = generate_unique_slug(instance=obj)
            obj.save(update_fields=['slug'])

        return obj
