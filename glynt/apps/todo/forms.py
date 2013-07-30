# -*- coding: UTF-8 -*-
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from parsley.decorators import parsleyfy

from .models import ToDo, Attachment


class AttachmentForm(forms.ModelForm):
    project = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Attachment


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

    def save(self, **kwargs):
        
        super(CutomerToDoForm, self).save(**kwargs)