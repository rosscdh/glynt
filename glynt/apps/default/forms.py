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

# ----- WILLS -----

class WillStep1(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'A little bit about yourself'}))
    gender = forms.ChoiceField(label='Are you male or female?',help_text='You should select a Gender',choices=(('female','Female'),('male','Male')),initial='female',widget=forms.RadioSelect(attrs={'placeholder':'Currency','class':'md-updater','data-hb-name':'gender'}))
    partnership = forms.ChoiceField(label='Are you married or are you in a civil partnership?',help_text='Should defacto not be here?',choices=(('false','Not Married'),('married','Married'),('civil_partnership','Civil Partnership')),initial='false',widget=forms.RadioSelect(attrs={'placeholder':'Partnership Type','class':'md-updater','data-hb-name':'partnership'}))
    executor =  forms.ChoiceField(label='Will you be appointing an Executor for this will other than your Partner (if any)',choices=(('false','No Executor'),('appoint_executor','Appoint Executor')),initial='false',widget=forms.RadioSelect(attrs={'placeholder':'Executor','class':'md-updater','data-hb-name':'executor'}))

class WillStep2(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Where do you live?'}))
    domicile = forms.ChoiceField(label='Where are you domiciled?',choices=(('england_wales','England and Wales'),('north_ireland','Northern Ireland')),widget=forms.RadioSelect(attrs={'placeholder':'Currency','class':'md-updater','data-hb-name':'domicile'}))
    partner_domicile = forms.ChoiceField(label='Where is your partner domiciled?',choices=(('england_wales','England and Wales'),('north_ireland','Northern Ireland')),widget=forms.RadioSelect(attrs={'placeholder':'Currency','class':'md-updater','data-hb-name':'partner_domicile'}))

class WillStep3(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'More Details'}))
    private_pension = forms.ChoiceField(label='Do you or your wife have a pension, other than a state pension, and/or a life assurance policy?',choices=(('yes','Yes'),('no','No')),widget=forms.RadioSelect(attrs={'placeholder':'Currency','class':'md-updater','data-hb-name':'private_pension'}))
    landowner = forms.ChoiceField(label='Do you and/or your wife own land or a property built on land (e.g. a house or flat)?',choices=(('yes','Yes'),('no','No')),widget=forms.RadioSelect(attrs={'placeholder':'Currency','class':'md-updater','data-hb-name':'landowner'}))

class WillStep4(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Your name & alias'}))
    full_name = forms.CharField(label='What is your full name?',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Your Full Name','class':'md-updater','data-hb-name':'full_name'}))
    other_alias = forms.CharField(label='If you are known by any other name, enter it here.',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Your Alias','class':'md-updater','data-hb-name':'other_alias'}))
    home_address = forms.CharField(label='What is your current home address?',widget=forms.Textarea(attrs={'placeholder':'Your Home Address','class':'md-updater','data-hb-name':'home_address'}))

class WillStep5(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Partner Details', 'data-glynt-rule':'[{show_step_when:{has_partnership:true}}]'}))
    partner_full_name = forms.CharField(label='What is your partners full name?',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Your Partner\'s Full Name','class':'md-updater','data-hb-name':'partner_full_name'}))
    partner_home_address = forms.CharField(label='What is your partners current home address?',widget=forms.Textarea(attrs={'placeholder':'Your Partner\'s Home Address','class':'md-updater','data-hb-name':'partner_home_address'}))

class WillStep6(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Executor Details', 'data-glynt-rule':'[{show_step_when:{has_executor:true}}]'}))
    executor_full_name = forms.CharField(label='What is full name of the executor you would like to appoint?',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Full Name of Executor','class':'md-updater','data-hb-name':'executor_full_name'}))
    executor_address = forms.CharField(label='What is your partners current home address?',widget=forms.Textarea(attrs={'placeholder':'Address of the Executor','class':'md-updater','data-hb-name':'executor_address'}))