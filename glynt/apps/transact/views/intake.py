# -*- coding: UTF-8 -*-
from glynt.apps.transact.forms import BasicInformationForm, CorporateAgentsForm, \
    InitialDirectorsForm, GeneralCapitalizationForm, CustomersForm, StockPlansForm, AboutCompanyBusinessForm, \
    IntellectualPropertyForm, EmployeesConsultantsForm


FORMS = [("basic_information", BasicInformationForm),
        ("corporate_agents", CorporateAgentsForm),
        ("initial_directors",InitialDirectorsForm),
        ("general_capitalization", GeneralCapitalizationForm),
        ("customers",CustomersForm),
        ("stock_plans", StockPlansForm),
        ("about_company_business", AboutCompanyBusinessForm),
        ("intellectual_property", IntellectualPropertyForm),
        ("employees_consultants", EmployeesConsultantsForm)]
