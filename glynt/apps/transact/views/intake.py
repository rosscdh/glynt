# -*- coding: UTF-8 -*-
from glynt.apps.transact.forms import CompanyProfileForm

# from glynt.apps.transact.forms import BasicInformationForm, CorporateAgentsForm, \
#     InitialDirectorsForm, GeneralCapitalizationForm, CustomersForm, StockPlansForm, AboutCompanyBusinessForm, \
#     IntellectualPropertyForm, EmployeesConsultantsForm

FORMS = [("company_profile", CompanyProfileForm), ]

# """
# STEP FORMS
# ----------
# format: (key, form, template, data_provider,)
# key: the key used to describe the set
# form: the form used to capture the data
# template: a specific template, should be None by default
# data_provider: a bunch/dict that provides data specific to this form
# """
# FORMS = [("basic_information", BasicInformationForm),
#         ("corporate_agents", CorporateAgentsForm),
#         ("initial_directors",InitialDirectorsForm),
#         ("general_capitalization", GeneralCapitalizationForm),
#         ("customers",CustomersForm),
#         ("stock_plans", StockPlansForm),
#         ("about_company_business", AboutCompanyBusinessForm),
#         ("intellectual_property", IntellectualPropertyForm),
#         ("employees_consultants", EmployeesConsultantsForm)]


TEMPLATES = []