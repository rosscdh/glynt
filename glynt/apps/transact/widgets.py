# -*- coding: UTF-8 -*-
from django import forms


class AddAnotherWidget(forms.TextInput):
    attrs = {}

    class Media:
        js = ('transact/js/widget-add_another.js',)
        css = {
            'all': ('transact/css/widget-add_another.css',)
        }
