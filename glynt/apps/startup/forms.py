# -*- coding: UTF-8 -*-
from django import forms
from bootstrap.forms import BootstrapMixin

from cicu.models import UploadedFile
from cicu.widgets import CicuUploderInput

from parsley.decorators import parsleyfy

from models import Startup, Founder

from services import EnsureFounderService, EnsureStartupService

import logging
logger = logging.getLogger('django.request')


@parsleyfy
class StartupProfileSetupForm(BootstrapMixin, forms.Form):
    """ Form to allow startups to enter basic information about 
    their setups
    """
    # django user ifo used to populate founder object
    first_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'First name', 'tabindex':'1'}))
    last_name = forms.CharField(help_text="", widget=forms.TextInput(attrs={'placeholder':'Last name','tabindex':'2'}))

    photo = forms.ImageField(required=False, label="Main Photo", help_text="Please add a good quality photo to your profile. It really helps.", widget=CicuUploderInput(attrs={'data-trigger':'change','data-required': 'false'}, options={
                'ratioWidth': '110',       #fix-width ratio, default 0
                'ratioHeight':'110',       #fix-height ratio , default 0
                'sizeWarning': 'False',    #if True the crop selection have to respect minimal ratio size defined above. Default 'False'
                'modalButtonLabel': 'Upload photo',
                'onReady': 'preparePhotoPreview',
                'onCrop': 'photoCrop'
            }))
    
    hidden_photo = forms.CharField(required=False, widget=forms.HiddenInput) # transports the id

    # startup
    startup_name = forms.CharField(label="Startup Name", help_text="", widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':'3'}))
    twitter = forms.CharField(required=False, label="Twitter", help_text="", widget=forms.TextInput(attrs={'tabindex':'6'}))
    summary = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'placeholder':'A brief description of your startup', 'tabindex':'4', 'class':'input-large', 'data-rangelength':'[0,1024]', 'rows':'2'}))
    website = forms.URLField(label="URL", help_text="", widget=forms.TextInput(attrs={'placeholder':'http://acmeco.com', 'class':'input-large', 'tabindex':'4'}))

    # capital details
    already_incorporated = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'7'}))
    already_raised_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'8'}))
    process_raising_capital = forms.BooleanField(required=False, label='', widget=forms.CheckboxInput(attrs={'tabindex':'9'}))
    incubator_or_accelerator_name  = forms.CharField(required=False, label='', help_text="", widget=forms.TextInput(attrs={'placeholder':'Incubator or accelerator name', 'tabindex':'10'}))

    agree_tandc = forms.BooleanField(label='', widget=forms.CheckboxInput(attrs={'tabindex':'11'}))

    def __init__(self, *args, **kwargs):
        """ get request object and user """
        self.request = kwargs.pop('request', None)
        self.user = self.request.user
        super(StartupProfileSetupForm, self).__init__(*args, **kwargs)

    def clean_hidden_photo(self):
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        return int(hidden_photo) if hidden_photo else None

    def save(self, commit=True):
        data = self.cleaned_data

        #self.user
        logger.info('StartupProfileSetupForm Starting')

        # @TODO should be in the clean_photo method
        hidden_photo = self.cleaned_data.get('hidden_photo', None)
        if type(hidden_photo) is int:
            try:
                data['photo'] = UploadedFile.objects.get(pk=hidden_photo)
            except UploadedFile.DoesNotExist:
                data['photo'] = None

        founder_service = EnsureFounderService(user=self.user, **data)
        founder = founder_service.process()

        startup_service = EnsureStartupService(name=data.get('startup_name'), founder=founder, **data)
        startup = startup_service.process()


class StartupProfileIsCompleteValidator(forms.Form):
    """ is used by the profile_complete template tag 
    to evaluate the completeness of a startups profile """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    startup_name = forms.CharField(required=True)


class FounderQuestionnaire(BootstrapMixin, forms.Form):
    # Basic Information
    company_name = forms.CharField(label="Company name", help_text="", widget=forms.TextInput(attrs={'placeholder':'Acme Inc', 'tabindex':''}))
    company_address = forms.CharField(label="Company address", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))
    company_phone = forms.CharField(label="Company address", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    fiscal_year_end = forms.DateField(label="Fiscal year end", help_text="", widget=forms.DateField(attrs={'tabindex':''}))
    brief_business_description = forms.CharField(label="Brief business description", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))

    # Corporate Agents
    agent_delaware_name = forms.CharField(label="Name", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    agent_delaware_address = forms.CharField(label="Address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    agent_california_name = forms.CharField(label="Name", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    agent_california_address = forms.CharField(label="Address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))

    # INITIAL DIRECTORS
    initial_number_of_directors = forms.IntegerField(label="Initial number of directors", help_text="", widget=forms.IntegerField(attrs={'tabindex':''}))
    names_of_directors = forms.CharField(label="Names of director(s)", help_text="", widget=forms.CharField(attrs={'tabindex':''}))

    # INITIAL OFFICERS
    president_or_chief_executive_officer = forms.CharField(label="President/Chief Executive Officer", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    secretary = forms.CharField(label="Secretary", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    treasurer_or_chief_financial_officer = forms.CharField(label="Treasurer/Chief Financial Office", widget=forms.CharField(attrs={'tabindex':''}))
    other_initial_officers = forms.CharField(label="Other", widget=forms.CharField(attrs={'tabindex':''}))

    # GENERAL CAPITALIZATION INFORMATION
    total_authorized_shares_of_common_stock = forms.CharField(label="Total authorized shares of common stock", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    par_value_per_share = forms.CharField(label="Par value per share", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    total_shares_to_be_purchased = forms.CharField(label="Total shares to be purchased by founders/initial investors", help_text="", widget=forms.CharField(attrs={'tabindex':''}))

    # FOUNDERS/INITIAL INVESTORS
    investor_name = forms.CharField(label="Name", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    investor_address = forms.CharField(label="Address", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    investor_phone = forms.CharField(label="Company address", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    investor_email = forms.CharField(label="Email", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    spouses_name = forms.CharField(label="Spouse’s name (if applicable)", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    work_visa = forms.CharField(label="Work Visa needed, or other immigration issues?", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    shares_to_be_purchased = forms.CharField(label="Number of shares to be purchased", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    total_purchase_price = forms.CharField(label="Total purchase price", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    non_cash_considerations = forms.CharField(label="Description of any non-cash consideration to be paid (including any assignment of intellectual property)", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    VESTING_CHOICES = (
        ('FY', 'Four-year vesting, with 25% vested after one year and month-to-month vesting thereafter'),
        ('AS', 'All shares will be immediately vested'),
        ('OD', 'Other (describe)'),
    )
    vesting = forms.ChoiceField(choices= VESTING_CHOICES, label="Vesting", help_text="", widget=forms.ChoiceField(attrs={'tabindex':''}))
    vesting_describe = forms.CharField(label="Please describe vesting", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    vesting_commencement_date = forms.DateField(label="Vesting commencement date", help_text="", widget=forms.DateField(attrs={'tabindex':''}))
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
    Acceleration_of_vesting = forms.MultipleChoiceField(choices=ACCELERATION_OF_VESTING_CHOICES, label="Acceleration of vesting (check all that apply)", help_text="", widget=forms.MultipleChoiceField(attrs={'tabindex':''}))

    # INFORMATION REGARDING STOCK PLAN
    equity_incentive_plan = forms.BooleanField(label="Will the company have an equity incentive plan?", help_text="", widget=forms.BooleanField())
    # IF YES:
    shares_authorized = forms.CharField(label="Name", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    GENERAL_VESTING_CHOICES = (
        ('FY', 'Four-year vesting, with 25% vested after one year and month-to-month vesting thereafter'),
        ('OD', 'Other (describe)'),
    )
    general_vesting_terms = forms.ChoiceField(choices=GENERAL_VESTING_CHOICES, label="General vesting terms for options", widget=forms.ChoiceField(attrs={'tabindex':''}))

    # INFORMATION ABOUT THE COMPANY’S BUSINESS
    date_company_begins_business = forms.DateField(label="Date on which the company will begin doing business", help_text="", widget=forms.DateField(attrs={'tabindex':''}))
    states_countries_doing_business = forms.CharField(label="States and countries in which the company will be doing business", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    detailed_business_description = forms.CharField(label="Detailed business description (e.g., describe the principal line of merchandise sold, products produced, services provided, etc.)", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))

    # INFORMATION CONCERNING INTELLECTUAL PROPERTY
    intellectual_property = forms.CharField(label="List any patents, copyrights and trademarks that the company will own or license and/or will want to register", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))
    domain_names_obtained = forms.BooleanField(label="Any Domain names obtained?", help_text="", widget=forms.BooleanField())
    # IF YES:
    domain_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    no_longer_affiliated = forms.BooleanField(label="Anyone involved in the creation of IP and no longer affiliated with the Company?", help_text="", widget=forms.BooleanField())
    # IF YES:
    no_longer_affiliated_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    others_involved = forms.BooleanField(label="Anyone other than the founders listed above involved in the creation of IP?", help_text="", widget=forms.BooleanField())
    # IF YES:
    others_involved_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.CharField(attrs={'tabindex':''}))
    university_affiliation = forms.BooleanField(label="Anyone involved in the creation of IP affiliated with a university at the time?", help_text="", widget=forms.BooleanField())
    # IF YES:
    university_affiliation_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.CharField(attrs={'tabindex':''}))