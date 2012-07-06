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
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Company Information'}))
    company_name = forms.CharField(label='What is the company name?',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Full Company Name','class':'md-updater','data-hb-name':'full_company_name'}))
    date_start = forms.DateField(label='Date of this agreement',widget=forms.DateInput(attrs={'placeholder':'23rd March 2013','class':'md-updater','data-hb-name':'date_start'}))
    company_street_address = forms.CharField(label='What is your street address of the company?',widget=forms.Textarea(attrs={'placeholder':'Your companies registered address','class':'md-updater','data-hb-name':'company_street_address','rows':'4'}))
    company_city = forms.CharField(label='What is the city of the company?',widget=forms.TextInput(attrs={'placeholder':'Your company registered city','class':'md-updater','data-hb-name':'company_city'}))
    company_state = forms.CharField(label='What is the state of the company?',widget=forms.TextInput(attrs={'placeholder':'State','class':'md-updater','data-hb-name':'company_state'}))
    company_zip = forms.CharField(label='What is the Zip code of the company?',widget=forms.TextInput(attrs={'placeholder':'Zip','class':'md-updater','data-hb-name':'company_zip'}))
    company_date_incorp = forms.CharField(label='When was the company incorporated?',widget=forms.TextInput(attrs={'placeholder':'21st March 2012','class':'md-updater','data-hb-name':'company_date_incorp'}))

class WillStep2(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Number of Shareholders', 'data-glynt-loop_step':"[{hide_from:'num_shareholders',iteration_title:'Shareholder'}]"}))
    num_shareholders = forms.ChoiceField(label='How many shareholders are there in your company?',choices=(('0','-----'),('1','1'),('2','2'),('3','3'),('4','4'),),initial=0, widget=forms.Select(attrs={'data-glynt-loop_length':''}))
    shareholder_type = forms.ChoiceField(label='Is the shareholder a company?',choices=(('company','Yes'),('person','No')),widget=forms.RadioSelect(attrs={'class':'md-updater','data-hb-name':'shareholder_type'}))
    shareholder_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Shareholder Name','class':'md-updater','data-hb-name':'shareholder_name'}))
    shareholder_address = forms.CharField(max_length=255,widget=forms.Textarea(attrs={'placeholder':'Shareholder Address including Zip','class':'md-updater','data-hb-name':'shareholder_address'}))
    shareholder_shares = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder':'Number of shares held','class':'md-updater','data-hb-name':'shareholder_shares'}))

class WillStep3(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'About the company'}))
    company_country = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Company country','class':'md-updater','data-hb-name':'company_country'}))
    company_activites = forms.CharField(max_length=255,widget=forms.Textarea(attrs={'placeholder':'Main activities of the company','class':'md-updater','data-hb-name':'company_activites'}))

class WillStep4(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Appointed Directors'}))
    company_director_noms = forms.CharField(label='How many directors may each shareholder nominate?',max_length=255, widget=forms.TextInput(attrs={'placeholder':'2','class':'md-updater','data-hb-name':'company_director_noms'}))
    company_max_directors = forms.CharField(label='What is the maximum number of Directors that can hold office at any one time?',max_length=255,widget=forms.TextInput(attrs={'placeholder':'e.g. 5','class':'md-updater','data-hb-name':'company_max_directors'}))
    company_management_account_freq = forms.CharField(label='How often are the management accounts to be prepared and sent to directors?',max_length=255,widget=forms.TextInput(attrs={'placeholder':'Quarterly','class':'md-updater','data-hb-name':'company_management_account_freq'}))
    company_meeting_freq = forms.CharField(label='How often must a director hold a meeting?',max_length=255,widget=forms.TextInput(attrs={'placeholder':'Monthly','class':'md-updater','data-hb-name':'company_meeting_freq'}))


class WillStep5(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Shareholder Nominations', 'data-glynt-loop_step':"[{hide_from:'num_direct_noms_from_shareholders',iteration_title:'Shareholder nom'}]"}))
    num_direct_noms_from_shareholders = forms.ChoiceField(label='Many any shareholders nominate additional directors?',choices=(('0','None'),('1','1'),('2','2'),('3','3'),('4','4'),),initial=0, widget=forms.Select(attrs={'data-glynt-loop_length':''}))
    shareholder_nom_name = forms.CharField(label='Shareholder name',max_length=255, widget=forms.TextInput(attrs={'placeholder':'Shareholder Name','class':'md-updater','data-hb-name':'shareholder_nom_name'}))
    shareholder_nom_allowed = forms.CharField(label='How many directors may they nominate?',max_length=255,widget=forms.TextInput(attrs={'placeholder':'1','class':'md-updater','data-hb-name':'shareholder_nom_allowed'}))


class WillStep6(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Share Allocation'}))
    shares_in_issue = forms.CharField(label='How many shares were in issue?',max_length=255, widget=forms.TextInput(attrs={'placeholder':'100','class':'md-updater','data-hb-name':'shares_in_issue'}))
    share_value = forms.CharField(label='What is the nominal share value?',max_length=255, widget=forms.TextInput(attrs={'placeholder':'$5','class':'md-updater','data-hb-name':'share_value'}))


class WillStep7(forms.Form):
    step_title = forms.CharField(max_length=100, widget=forms.HiddenInput(attrs={'data-step-title':'Misc Details'}))
    max_cap = forms.CharField(label='What is the maximum amount of capital expenditure that may be incurred before there must be unanimous agreement by the shareholders?',max_length=255, widget=forms.TextInput(attrs={'placeholder':'$500','class':'md-updater','data-hb-name':'max_cap'}))
    how_many_days = forms.CharField(label='How many days do the Shareholders have to make an offer for the shares?',max_length=255, widget=forms.TextInput(attrs={'placeholder':'28','class':'md-updater','data-hb-name':'how_many_days'}))
    how_many_days_sealed = forms.CharField(label='How many days shall the Shareholders have in which to make a sealed bid?',max_length=255, widget=forms.TextInput(attrs={'placeholder':'28','class':'md-updater','data-hb-name':'how_many_days_sealed'}))
    how_many_days_to_pay = forms.CharField(label='Within how many days does the money for the shares have to be paid??',max_length=255, widget=forms.TextInput(attrs={'placeholder':'60','class':'md-updater','data-hb-name':'how_many_days_pay'}))
