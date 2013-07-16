# -*- coding: UTF-8 -*-
from glynt.apps.transact.forms import BasicInformationForm, CorporateAgentsForm, \
    InitialDirectorsForm, GeneralCapitalizationForm, CustomersForm, StockPlansForm, AboutCompanyBusinessForm, \
    IntellectualPropertyForm, EmployeesConsultantsForm


"""
STEP FORMS
----------
format: (key, form, template, data_provider,)
key: the key used to describe the set
form: the form used to capture the data
template: a specific template, should be None by default
data_provider: a bunch/dict that provides data specific to this form
"""
FORMS = [("basic_information", BasicInformationForm, None, {}),
        ("corporate_agents", CorporateAgentsForm, None, {}),
        ("initial_directors",InitialDirectorsForm, None, {}),
        ("general_capitalization", GeneralCapitalizationForm, None, {}),
        ("customers",CustomersForm, None, {}),
        ("stock_plans", StockPlansForm, None, {}),
        ("about_company_business", AboutCompanyBusinessForm, None, {}),
        ("intellectual_property", IntellectualPropertyForm, None, {}),
        ("employees_consultants", EmployeesConsultantsForm, None, {}),]
