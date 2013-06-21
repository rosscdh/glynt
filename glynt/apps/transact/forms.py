# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy


# WIZARD STEP ONE
class PackagesForm(BootstrapMixin, forms.Form):
    TRANSACTION_CHOICES = (
        ('CS', 'Company Setup'),
        ('ES', 'Equity seed financing'),
        ('SF', 'Convertible seed financing'),
    )
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, widget=forms.HiddenInput())


# WIZARD STEP TWO
class BasicInformationForm(BootstrapMixin, forms.Form):
    contact_name = forms.CharField(label="Contact name", help_text="", widget=forms.TextInput(attrs={'tabindex':'1'}))
    company_address = forms.CharField(label="Company address", help_text="Please enter you full street address including post code.", widget=forms.Textarea(attrs={'tabindex':'2'}))
    company_email = forms.EmailField(label="Contact email address", widget=forms.TextInput(attrs={'tabindex':'3'}))
    telephone = forms.CharField(label="Telephone number", help_text="", widget=forms.TextInput(attrs={'tabindex':'4'}))
    PRIMARY_CONTACT_CHOICES = (
        ('ME','Me'),
        ('SE','Someone else'),
    )
    primary_contact = forms.ChoiceField(choices=PRIMARY_CONTACT_CHOICES, label="Primary contact person", help_text="", widget=forms.RadioSelect(attrs={'tabindex':'5'}))
    fiscal_year_end = forms.DateField(label="Fiscal year end", help_text="", widget=forms.DateInput(attrs={'tabindex':'6'}))


# WIZARD STEP THREE
class OtherAgreementsForm(BootstrapMixin, forms.Form):
    agreement_details = forms.CharField(label="Enter details here", help_text="", widget=forms.Textarea())


# FOR REF...

class FounderQuestionnaire(BootstrapMixin, forms.Form):
    # Basic Information
    company_name = forms.CharField(label="Company name", help_text="", widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':''}))
    company_address = forms.CharField(label="Company address", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))
    company_phone = forms.CharField(label="Company address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    fiscal_year_end = forms.DateField(label="Fiscal year end", help_text="", widget=forms.DateInput(attrs={'tabindex':''}))
    brief_business_description = forms.CharField(label="Brief business description", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))

    # Corporate Agents
    agent_delaware_name = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    agent_delaware_address = forms.CharField(label="Address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    agent_california_name = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    agent_california_address = forms.CharField(label="Address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))

    # INITIAL DIRECTORS
    initial_number_of_directors = forms.IntegerField(label="Initial number of directors", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    names_of_directors = forms.CharField(label="Names of director(s)", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))

    # INITIAL OFFICERS
    president_or_chief_executive_officer = forms.CharField(label="President/Chief Executive Officer", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    secretary = forms.CharField(label="Secretary", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    treasurer_or_chief_financial_officer = forms.CharField(label="Treasurer/Chief Financial Office", widget=forms.TextInput(attrs={'tabindex':''}))
    other_initial_officers = forms.CharField(label="Other", widget=forms.TextInput(attrs={'tabindex':''}))

    # GENERAL CAPITALIZATION INFORMATION
    total_authorized_shares_of_common_stock = forms.CharField(label="Total authorized shares of common stock", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    par_value_per_share = forms.CharField(label="Par value per share", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    total_shares_to_be_purchased = forms.CharField(label="Total shares to be purchased by founders/initial investors", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))

    # FOUNDERS/INITIAL INVESTORS
    investor_name = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    investor_address = forms.CharField(label="Address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    investor_phone = forms.CharField(label="Company address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    investor_email = forms.CharField(label="Email", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    spouses_name = forms.CharField(label="Spouse’s name (if applicable)", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    work_visa = forms.CharField(label="Work Visa needed, or other immigration issues?", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    shares_to_be_purchased = forms.CharField(label="Number of shares to be purchased", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    total_purchase_price = forms.CharField(label="Total purchase price", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    non_cash_considerations = forms.CharField(label="Description of any non-cash consideration to be paid (including any assignment of intellectual property)", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    VESTING_CHOICES = (
        ('FY', 'Four-year vesting, with 25% vested after one year and month-to-month vesting thereafter'),
        ('AS', 'All shares will be immediately vested'),
        ('OD', 'Other (describe)'),
    )
    vesting = forms.ChoiceField(choices= VESTING_CHOICES, label="Vesting", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    vesting_describe = forms.CharField(label="Please describe vesting", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    vesting_commencement_date = forms.DateField(label="Vesting commencement date", help_text="", widget=forms.DateInput(attrs={'tabindex':''}))
    ACCELERATION_OF_VESTING_CHOICES = (
        ('DT','Double trigger (i.e., acceleration upon termination without “cause” after a change of control)'),
        ('PS', 'Percentage of shares accelerated on double trigger'),
        ('MT', 'Number of months after a change of control during which a termination without “cause” will result in an acceleration of vesting'),
        ('ST','Single trigger – change of control'),
        ('PA', 'Percentage of shares accelerated on single trigger'),
        ('TC','Single trigger – termination without cause or leaving for good reason'),
        ('SA', 'Percentage of shares accelerated on single trigger'),
        ('NA', 'No acceleration of vesting'),
    )
    Acceleration_of_vesting = forms.MultipleChoiceField(choices=ACCELERATION_OF_VESTING_CHOICES, label="Acceleration of vesting (check all that apply)", help_text="", widget=forms.SelectMultiple(attrs={'tabindex':''}))

    # INFORMATION REGARDING STOCK PLAN
    equity_incentive_plan = forms.BooleanField(label="Will the company have an equity incentive plan?", help_text="", widget=forms.Select())
    # IF YES:
    shares_authorized = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    GENERAL_VESTING_CHOICES = (
        ('FY', 'Four-year vesting, with 25% vested after one year and month-to-month vesting thereafter'),
        ('OD', 'Other (describe)'),
    )
    general_vesting_terms = forms.ChoiceField(choices=GENERAL_VESTING_CHOICES, label="General vesting terms for options", widget=forms.Select(attrs={'tabindex':''}))

    # INFORMATION ABOUT THE COMPANY’S BUSINESS
    date_company_begins_business = forms.DateField(label="Date on which the company will begin doing business", help_text="", widget=forms.DateInput(attrs={'tabindex':''}))
    states_countries_doing_business = forms.CharField(label="States and countries in which the company will be doing business", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    detailed_business_description = forms.CharField(label="Detailed business description (e.g., describe the principal line of merchandise sold, products produced, services provided, etc.)", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))

    # INFORMATION CONCERNING INTELLECTUAL PROPERTY
    intellectual_property = forms.CharField(label="List any patents, copyrights and trademarks that the company will own or license and/or will want to register", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))
    domain_names_obtained = forms.BooleanField(label="Any Domain names obtained?", help_text="", widget=forms.Select())
    # IF YES:
    domain_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    no_longer_affiliated = forms.BooleanField(label="Anyone involved in the creation of IP and no longer affiliated with the Company?", help_text="", widget=forms.Select())
    # IF YES:
    no_longer_affiliated_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    others_involved = forms.BooleanField(label="Anyone other than the founders listed above involved in the creation of IP?", help_text="", widget=forms.Select())
    # IF YES:
    others_involved_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    university_affiliation = forms.BooleanField(label="Anyone involved in the creation of IP affiliated with a university at the time?", help_text="", widget=forms.Select())
    # IF YES:
    university_affiliation_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))