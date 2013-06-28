# -*- coding: UTF-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML

from bootstrap.forms import BootstrapMixin

from parsley.decorators import parsleyfy


# WIZARD STEP ONE
class PackagesForm(forms.Form):
    transaction_type = forms.CharField(widget=forms.HiddenInput)


# WIZARD STEP TWO
@parsleyfy
class BasicInformationForm(forms.Form):
    company_name = forms.CharField(label="Company name", help_text="", widget=forms.TextInput(attrs={'tabindex':'1'}))
    company_address = forms.CharField(label="Company address", help_text="Please enter you full street address including post code.", widget=forms.Textarea(attrs={'tabindex':'2'}))
    company_phone = forms.CharField(label="Company phone", help_text="", widget=forms.TextInput(attrs={'tabindex':'3', 'data-type':'phone'}))
    fiscal_year_end = forms.DateField(label="Fiscal year end", help_text="", widget=forms.DateInput(attrs={'tabindex':'4', 'placeholder':'MM/DD/YY', 'data-americandate':'true'}))
    brief_business_description = forms.CharField(label="Brief business description", help_text="", widget=forms.Textarea(attrs={'tabindex':'5'}))
    electronic_signatures = forms.BooleanField(label="Would you like to use electronic signatures when possible to sign your legal docs?", required=False, help_text="", widget=forms.CheckboxInput(attrs={'tabindex':'6'}))


# WIZARD STEP THREE
@parsleyfy
class CorporateAgentsForm(forms.Form):
    agent_delaware_name = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':'1'}))
    agent_delaware_address = forms.CharField(label="Address", help_text="", widget=forms.Textarea(attrs={'tabindex':'2'}))
    agent_california_name = forms.CharField(label="Name", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':'3'}))
    agent_california_address = forms.CharField(label="Address", required=False, help_text="", widget=forms.Textarea(attrs={'tabindex':'4'}))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Registered agent in Delaware',
                'agent_delaware_name',
                'agent_delaware_address'
            ),
            Fieldset(
                'Agent for service of process in California (if applicable)',
                'agent_california_name',
                'agent_california_address'
            ),
            ButtonHolder(
                Submit('submit', 'Next', css_class='btn btn-success')
            )
        )
        super(CorporateAgentsForm, self).__init__(*args, **kwargs)


# WIZARD STEP FOUR
@parsleyfy
class InitialDirectorsForm(forms.Form):
    initial_number_of_directors = forms.IntegerField(label="Initial number of directors", help_text="", widget=forms.TextInput(attrs={'tabindex':'1'}))
    names_of_directors = forms.CharField(label="Names of director(s)", help_text="", widget=forms.TextInput(attrs={'tabindex':'2'}))

    # INITIAL OFFICERS
    president_or_chief_executive_officer = forms.CharField(label="President/Chief Executive Officer", help_text="", widget=forms.TextInput(attrs={'tabindex':'3'}))
    secretary = forms.CharField(label="Secretary", help_text="", widget=forms.TextInput(attrs={'tabindex':'4'}))
    treasurer_or_chief_financial_officer = forms.CharField(label="Treasurer/Chief Financial Office", widget=forms.TextInput(attrs={'tabindex':'5'}))
    other_initial_officer = forms.CharField(label="Other", required=False, widget=forms.TextInput(attrs={'tabindex':'6'}))
    other_initial_officers = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Initial Directors',
                'initial_number_of_directors',
                'names_of_directors',
            ),
            Fieldset(
                'Initial Officers',
                'president_or_chief_executive_officer',
                'secretary',
                'treasurer_or_chief_financial_officer',
                'other_initial_officer',
                'other_initial_officers',
                HTML("""
            <p><a href="#" class="add-field" data-target-field="id_initial_directors-other_initial_officer">Add another</a></p>
        """)),
            ButtonHolder(
                Submit('submit', 'Next', css_class='btn btn-success')
            )
        )
        super(InitialDirectorsForm, self).__init__(*args, **kwargs)


# WIZARD STEP FIVE
@parsleyfy
class GeneralCapitalizationForm(forms.Form):
    total_authorized_shares_of_common_stock = forms.CharField(label="Total authorized shares of common stock", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    par_value_per_share = forms.CharField(label="Par value per share", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    total_shares_founders = forms.CharField(label="Total shares to be purchased by founders", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    price_paid_founders = forms.CharField(label="Price per share to be paid by founders", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))


# WIZARD STEP SIX
@parsleyfy
class FoundersForm(forms.Form):
    first_name = forms.CharField(label="First name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    last_name = forms.CharField(label="Last name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    address = forms.CharField(label="Address", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    phone = forms.CharField(label="Company address", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    email = forms.CharField(label="Email", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    spouses_name = forms.CharField(label="Spouse’s name (if applicable)", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    work_visa = forms.CharField(label="Work Visa needed, or other immigration issues?", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    shares_to_be_purchased = forms.CharField(label="Number of shares to be purchased", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    total_purchase_price = forms.CharField(label="Total purchase price", help_text="", required=False, widget=forms.TextInput(attrs={'tabindex':''}))
    non_cash_considerations = forms.CharField(label="Description of any non-cash consideration to be paid (including any assignment of intellectual property)", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    VESTING_CHOICES = (
        ('FY', 'Four-year vesting, with 25% vested after one year and month-to-month vesting thereafter'),
        ('AS', 'All shares will be immediately vested'),
        ('OD', 'Other (describe)'),
    )
    vesting = forms.ChoiceField(choices= VESTING_CHOICES, required=False, label="Vesting", help_text="", widget=forms.Select(attrs={'tabindex':''}))
    vesting_describe = forms.CharField(label="Please describe vesting", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    vesting_commencement_date = forms.DateField(label="Vesting commencement date", required=False, help_text="", widget=forms.DateInput(attrs={'tabindex':''}))

    # Acceleration of vesting
    double_trigger = forms.BooleanField(label="Double trigger (i.e., acceleration upon termination without “cause” after a change of control)", required=False, help_text="", widget=forms.CheckboxInput(attrs={'tabindex':''}))
    dt_percentage_of_shares = forms.CharField(label="Percentage of shares accelerated on double trigger", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    dt_months_termination = forms.CharField(label="Number of months after a change of control during which a termination without “cause” will result in an acceleration of vesting", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    single_trigger_change = forms.BooleanField(label="Single trigger – change of control", required=False, help_text="", widget=forms.CheckboxInput(attrs={'tabindex':''}))
    st_percentage_of_shares = forms.CharField(label="Percentage of shares accelerated on single trigger", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    single_trigger_termination = forms.BooleanField(label="Single trigger – termination without cause or leaving for good reason", required=False, help_text="", widget=forms.CheckboxInput(attrs={'tabindex':''}))
    st_termination_percentage_of_shares = forms.CharField(label="Percentage of shares accelerated on single trigger", required=False, help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    no_acceleration = forms.BooleanField(label="No acceleration of vesting", required=False, help_text="", widget=forms.CheckboxInput(attrs={'tabindex':''}))

    founders = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Founder Details',
                'first_name',
                'last_name',
                'address',
                'phone',
                'email',
                'spouses_name',
                'work_visa',
                'shares_to_be_purchased',
                'total_purchase_price',
                'non_cash_considerations',
            ),
            Fieldset(
                'Vesting Details',
                'vesting',
                'vesting_describe',
                'vesting_commencement_date',
                'double_trigger',
                'dt_percentage_of_shares',
                'dt_months_termination',
                'single_trigger_change',
                'st_percentage_of_shares',
                'single_trigger_termination',
                'st_termination_percentage_of_shares',
                'no_acceleration',
            ),
            'founders'
        )
        super(FoundersForm, self).__init__(*args, **kwargs)


# WIZARD STEP SEVEN
class StockPlansForm(BootstrapMixin, forms.Form):
    equity_incentive_plan = forms.BooleanField(label="Will the company have an equity incentive plan?", help_text="", widget=forms.CheckboxInput())
    # IF YES:
    shares_authorized = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    GENERAL_VESTING_CHOICES = (
        ('FY', 'Four-year vesting, with 25% vested after one year and month-to-month vesting thereafter'),
        ('OD', 'Other (describe)'),
    )
    general_vesting_terms = forms.ChoiceField(choices=GENERAL_VESTING_CHOICES, label="General vesting terms for options", widget=forms.Select(attrs={'tabindex':''}))
    # IF OTHER:
    general_vesting_other = forms.CharField(label="Please describe", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))

    # Information regarding grantees located in the United States (NEEDS TO ALLOW FOR MULTIPLES)
    grantee_name = forms.CharField(label="Name of Grantee", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    employee_consultant_advisor = forms.CharField(label="Employee/Consultant/Advisor", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    num_options_granted = forms.CharField(label="Number of Options Granted", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    grantee_state_locale = forms.CharField(label="State where grantee is located", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))


# WIZARD STEP EIGHT
class AboutCompanyBusinessForm(BootstrapMixin, forms.Form):
    date_company_begins_business = forms.DateField(label="Date on which the company will begin doing business", help_text="", widget=forms.DateInput(attrs={'tabindex':''}))
    states_countries_doing_business = forms.CharField(label="States and countries in which the company will be doing business", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    detailed_business_description = forms.CharField(label="Detailed business description (e.g., describe the principal line of merchandise sold, products produced, services provided, etc.)", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))


# WIZARD STEP NINE
class IntellectualPropertyForm(BootstrapMixin, forms.Form):
    intellectual_property = forms.CharField(label="List any patents, copyrights and trademarks that the company will own or license and/or will want to register", help_text="", widget=forms.Textarea(attrs={'tabindex':''}))
    domain_names_obtained = forms.BooleanField(label="Any Domain names obtained?", help_text="", widget=forms.CheckboxInput())
    # IF YES:
    domain_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    no_longer_affiliated = forms.BooleanField(label="Anyone involved in the creation of IP and no longer affiliated with the Company?", help_text="", widget=forms.CheckboxInput())
    # IF YES:
    no_longer_affiliated_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    others_involved = forms.BooleanField(label="Anyone other than the founders listed above involved in the creation of IP?", help_text="", widget=forms.CheckboxInput())
    # IF YES:
    others_involved_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))
    university_affiliation = forms.BooleanField(label="Anyone involved in the creation of IP affiliated with a university at the time?", help_text="", widget=forms.CheckboxInput())
    # IF YES:
    university_affiliation_details = forms.CharField(label="If yes, please detail", help_text="", widget=forms.TextInput(attrs={'tabindex':''}))


# WIZARD STEP TEN
class EmployeesConsultantsForm(BootstrapMixin, forms.Form):
    name = forms.CharField(label="Name", help_text="", widget=forms.TextInput(attrs={'tabindex':'1'}))
    EMPLOYMENT_TYPE_CHOICES = (
        ('EM', 'Employee'),
        ('CO', 'Consultant'),
    )
    employment_type = forms.ChoiceField(choices= EMPLOYMENT_TYPE_CHOICES, label="Vesting", help_text="", widget=forms.Select(attrs={'tabindex':''}))
    scope_of_work = forms.CharField(label="Scope of Work", help_text="", widget=forms.TextInput(attrs={'tabindex':'1'}))


#class OtherAgreementsForm(BootstrapMixin, forms.Form):
#    agreement_details = forms.CharField(required=False, label="Enter details here", help_text="", widget=forms.Textarea())


#class ExistingDocumentationForm(BootstrapMixin, forms.Form):
#    dummy_file = forms.CharField(required=False, widget=forms.HiddenInput())