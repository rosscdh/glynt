# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from parsley.decorators import parsleyfy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div

from glynt.apps.transact import BuilderBaseForm, CrispyExFieldsetFieldRemovalMixin
from glynt.apps.company import COMPANY_STATUS_CHOICES
from glynt.apps.company import OPTION_PLAN_STATUS_CHOICES


@parsleyfy
class CompanyProfileForm(BuilderBaseForm):
    """
    The Company Setup Form
    This form only appears if they are doing an incorporation only. 

    """
    page_title = 'Your Company Profile'
    page_description = 'Enter some basic details about your company'
    #data_bag = 'glynt.apps.company.bunches.UserIntakeCompanyBunch'

    founder_name = forms.CharField()
    founder_email = forms.EmailField()

    incubator = forms.CharField(label=_('Incubator or accelerator'), required=False, help_text="If you are currently particpating in an accelerator please enter it here.")
    current_status = forms.ChoiceField(label=_('Current funding status'), choices=COMPANY_STATUS_CHOICES.get_choices(), initial=COMPANY_STATUS_CHOICES.pre_funding, widget=forms.RadioSelect)
    profile_website = forms.URLField(label=_('Website or other profile'), help_text="", widget=forms.TextInput(attrs={'data-type': 'url', 'placeholder': 'http://angel.co/lawpal'}))
    description = forms.CharField(label=_('Short description of startup'), required=False, help_text="Skip this if you have entered a website or AngelList profile")
    option_plan_status = forms.ChoiceField(label=_('Option plan'), choices=OPTION_PLAN_STATUS_CHOICES.get_choices(), initial=OPTION_PLAN_STATUS_CHOICES.would_like, widget=forms.RadioSelect)

    target_states_and_countries = forms.CharField(label=_('Where will you do business?'), initial="California", help_text="e.g. California, New York. Separate with a comma.", widget=forms.TextInput(attrs={'placeholder': 'California'}))
    num_officers = forms.CharField(label=_('Number of Directors and Officers'), initial=1, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_employees = forms.CharField(label=_('Number of employees'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_consultants = forms.CharField(label=_('Number of consultants'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_option_holders = forms.CharField(label=_('Number of option holders'), initial=0, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    ip_nolonger_affiliated = forms.BooleanField(label=_('Someone involved in the creation of IP is no longer affiliated with the Company'), required=False, initial=False)
    ip_otherthan_founder = forms.BooleanField(label=_('Someone other than the founders listed was involved in the creation of IP'), required=False, initial=False)
    ip_university_affiliation = forms.BooleanField(label=_('Someone involved in the creation of IP was affiliated with a university at the time'), required=False, initial=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Founding Team',
                Div(
                    'founder_name',
                    'founder_email',
                    **{'class': 'founder-group clearfix'}
                ),
                **{'data-region-clone': 'true', 'data-region-name': 'founders', 'class': 'founder-block clearfix'}
            ),
            Fieldset(
                'About your Startup',
                'incubator',
                'current_status',
                'profile_website',
                'description',
                'target_states_and_countries',
                'num_officers',
                'num_employees',
                'num_consultants',
                'option_plan_status',
                'num_option_holders',
                'ip_nolonger_affiliated',
                'ip_otherthan_founder',
                'ip_university_affiliation',
            )
        )
        super(CompanyProfileForm, self).__init__(*args, **kwargs)

    def get_update_url(self, **kwargs):
        return '/api/v1/company/data/{pk}'.format(pk=kwargs.get('project').company.pk)


@parsleyfy
class FinancingProfileForm(BuilderBaseForm):
    """
    The Financing Setup Form (if they select either seed financing equity or convertible only)
    """
    page_title = 'Financing Questions'
    page_description = 'Enter some basic details about your finance round requirements'

    founder_name = forms.CharField()
    founder_email = forms.EmailField()

    investment_terms = forms.CharField(label=_('Investment terms'), required=False, help_text="Briefly describe the source(s) and terms of your investment", widget=forms.Textarea)
    num_investors = forms.CharField(label=_('Number of investors'), initial=1, widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
    num_investor_states = forms.CharField(label=_('Number of investor states'), initial=1, help_text="The number of seperate states that your investors reside in", widget=forms.TextInput(attrs={'data-type': 'number', 'class': 'input-smaller'}))
 
    incubator = forms.CharField(label=_('Incubator or accelerator'), required=False, help_text="If you are currently particpating in an accelerator please enter it here.")
    already_incorp = forms.BooleanField(label=_('We have already incorporated'), required=False, initial=False)

    doc_exists_cert_incorm = forms.BooleanField(label=_('Certificate of Incorporation'), required=False, initial=True)
    doc_exists_action_written_consent = forms.BooleanField(label=_('Action by Written Consent of Incorporator'), required=False, initial=True)
    doc_exists_initial_written_consent = forms.BooleanField(label=_('Initial Written Consent of Board in Lieu of First Meeting'), required=False, initial=True)
    doc_exists_bylaws = forms.BooleanField(label=_('Bylaws'), required=False, initial=True)
    doc_exists_shareholder_agr = forms.BooleanField(label=_('Shareholder Agreement'), required=False, initial=True)
    doc_exists_ein_letter = forms.BooleanField(label=_('EIN Assignment Letter from the IRS'), required=False, initial=True)
    doc_exists_stock_purchase_agreement = forms.BooleanField(label=_('Stock Purchase Agreement for each founder'), required=False, initial=True)
    doc_exists_ip_assignment = forms.BooleanField(label=_('Confidential Information and Invention Assignment Agreement for each Founder'), required=False, initial=True)
    doc_exists_notice_of_stock_issuance = forms.BooleanField(label=_('Notice of Stock Issuance for each founder '), required=False, initial=True)
    doc_exists_stock_certs = forms.BooleanField(label=_('Stock Certificate for each Founder'), required=False, initial=True)
    doc_exists_83b = forms.BooleanField(label=_('83(b) Election for each Founder'), required=False, initial=True)
    doc_exists_stock_option_plan = forms.BooleanField(label=_('Stock Option Plan'), required=False, initial=True)


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Founding Team',
                Div(
                    'founder_name',
                    'founder_email',
                    **{'class': 'founder-group clearfix'}
                ),
                **{'data-region-clone': 'true', 'data-region-name': 'founders', 'class': 'founder-block clearfix'}
            ),
            Fieldset(
                'About Your Round',
                'investment_terms',
                'num_investors',
                'num_investor_states',
                'incubator',
                'already_incorp',
            ),
            # @todo Only show this fieldset if Already incorp is true
            Fieldset(
                'Which of the following do you have?',
                'doc_exists_cert_incorm',
                'doc_exists_action_written_consent',
                'doc_exists_initial_written_consent', 
                'doc_exists_bylaws', 
                'doc_exists_shareholder_agr', 
                'doc_exists_ein_letter',
                'doc_exists_stock_purchase_agreement',
                'doc_exists_ip_assignment',
                'doc_exists_notice_of_stock_issuance',
                'doc_exists_stock_certs', 
                'doc_exists_83b', 
                'doc_exists_stock_option_plan'
            )
        )
        super(FinancingProfileForm, self).__init__(*args, **kwargs)


@parsleyfy
class CompanyAndFinancingProfileForm(CrispyExFieldsetFieldRemovalMixin, CompanyProfileForm, FinancingProfileForm):
    """
    The Setup AND Financing Form (both selected)
    Basically we are combining the two forms and only showing the following fields. Not sure how to code this. 
    """
    page_title = 'Company & Financing Questions'
    page_description = 'Enter some basic details about your company and your finance round requirements'

    def __init__(self, *args, **kwargs):
        super(CompanyAndFinancingProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper() if not self.helper else self.helper

        self.helper.layout = Layout(
            Fieldset(
                'Founding Team',
                Div(
                    'founder_name',
                    'founder_email',
                    **{'class': 'founder-group clearfix'}
                ),
                **{'data-region-clone': 'true', 'data-region-name': 'founders', 'class': 'founder-block clearfix'}
            ),
            Fieldset(
                'About Your Round',
                'investment_terms',
                'num_investors',
                'num_investor_states',
                'incubator',
                'already_incorp',
            ),
            Fieldset(
                'About your Startup',
                'incubator',
                'current_status',
                'profile_website',
                'description',
                'target_states_and_countries',
                'num_officers',
                'num_employees',
                'num_consultants',
                'option_plan_status',
                'num_option_holders',
                'ip_nolonger_affiliated',
                'ip_otherthan_founder',
                'ip_university_affiliation',
            ),
            Fieldset(
                'Which of the following do you have?',
                'doc_exists_cert_incorm',
                'doc_exists_action_written_consent',
                'doc_exists_initial_written_consent', 
                'doc_exists_bylaws', 
                'doc_exists_shareholder_agr', 
                'doc_exists_ein_letter',
                'doc_exists_stock_purchase_agreement',
                'doc_exists_ip_assignment',
                'doc_exists_notice_of_stock_issuance',
                'doc_exists_stock_certs', 
                'doc_exists_83b', 
                'doc_exists_stock_option_plan'
            )
        )
        self.unify_fields()