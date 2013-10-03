# -*- coding: UTF-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from parsley.decorators import parsleyfy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit

from .models import Project

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
                Submit('send', 'Send', css_id='send-contact-us-modal'),
                css_class='modal-footer',
            ),
        ))

        super(ContactUsForm, self).__init__(*args, **kwargs)


class CreateProjectForm(forms.Form):
    transaction_type = forms.CharField(widget=forms.HiddenInput)


@parsleyfy
class ProjectCategoryForm(forms.ModelForm):
    """
    Form used to add/edit categories to projects
    """
    data = forms.CharField(required=True, widget=forms.HiddenInput)
    category = forms.CharField(required=True)

    class Meta:
        model = Project
        fields = ('data',)

    def __init__(self, *args, **kwargs):
        project_uuid = kwargs.pop('project_uuid')
        self.original_category = kwargs.pop('original_category')

        self.message = None
        self.added_message = 'Added category "{category}"'
        self.modified_message = 'Modified category "{original_category}"" to be "{category}"'

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'project-category'
        self.helper.form_method = 'post'

        self.helper.form_action = reverse('project:category', kwargs={'slug': project_uuid})

        self.helper.add_layout(Layout(
            Div(
                'General',
                'category',
                css_class='modal-body'
            )
        ))

        super(ProjectCategoryForm, self).__init__(*args, **kwargs)

    def clean_data(self):
        """
        just return the data field without validation or cleaning
        """
        return self.instance.data

    def clean_category(self):
        """
        clean logic for adding new categories
        should probably be a mixin
        """
        category = self.cleaned_data.get('category', None)
        # Used in the view
        self.category = category
        self.category_slug = slugify(category)

        categories = self.instance.categories

        # delete the old original category if present
        if self.original_category not in categories:
            # add
            if category is None:
                raise forms.ValidationError('Category cannot be None')
            else:
                # append new cat if not None
                categories.append(category)
                self.message = self.added_message.format(category=category)
        else:
            # edit
            categories.remove(self.original_category)
            # set the message
            self.message = self.modified_message.format(original_category=self.original_category, category=category)

        # set the instance categories to our updated
        # ensure uniquness by convert to set then back to list
        # cant use set as set loses sort order which is important here
        self.instance.categories = categories

        return category

    def save(self, **kwargs):
        if self.cleaned_data.get('category', None) in self.instance.categories:
            self.instance.save(update_fields=['data'])
