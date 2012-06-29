# -*- coding: utf-8 -*-
from django import forms

class AssassinStep1(forms.Form):
    contractor = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Your Name','class':'md-updater','data-hb-name':'contractor'}))
    cost = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'10,000.00','class':'md-updater','data-hb-name':'cost'}))
    currency = forms.ChoiceField(choices=(('€','€'),('£','£'),('$','$')),widget=forms.Select(attrs={'placeholder':'Currency','class':'md-updater','data-hb-name':'currency'}))
    target = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Target Name','class':'md-updater','data-hb-name':'target'}))
    date_by = forms.DateField(widget=forms.DateInput(attrs={'placeholder':'23rd March 2013','class':'md-updater','data-hb-name':'date_by'}))

class AssassinStep2(forms.Form):
    has_other_targets = forms.BooleanField(label='Do you have other targets?',widget=forms.CheckboxInput(attrs={'placeholder':'Do you have other targets?','class':'md-updater','data-hb-name':'has_other_targets'}))
    other_targets = forms.MultipleChoiceField(choices=(('Mark','Mark'),('James','James'),('John','John'),('Paul','Paul')),widget=forms.SelectMultiple(attrs={'placeholder':'','class':'md-updater','data-hb-name':'other_targets'}))
    confirmed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'placeholder':'','class':'md-updater','data-hb-name':'confirmed'}))

