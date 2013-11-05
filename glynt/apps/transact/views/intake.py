# -*- coding: UTF-8 -*-
from glynt.apps.company.forms import (CompanyProfileForm,
                                      CompanyAndFinancingProfileForm,
                                      FinancingProfileForm,
                                      GenericIntakeForm,
                                     )

# from glynt.apps.transact.forms import BasicInformationForm, CorporateAgentsForm, \
#     InitialDirectorsForm, GeneralCapitalizationForm, CustomersForm, StockPlansForm, AboutCompanyBusinessForm, \
#     IntellectualPropertyForm, EmployeesConsultantsForm

# INTAKE_FORMS = [("company_profile", CompanyProfileForm), ]

# Basic transactions
INC_FORMS = [("generic_intake", GenericIntakeForm), ]
FIN_FORMS = [("generic_intake", GenericIntakeForm), ]
IP_FORMS  = [("generic_intake", GenericIntakeForm), ]
IMM_FORMS = [("generic_intake", GenericIntakeForm), ]
EMP_FORMS = [("generic_intake", GenericIntakeForm), ]
NDA_FORMS = [("generic_intake", GenericIntakeForm), ]
PRI_FORMS = [("generic_intake", GenericIntakeForm), ]
OTH_FORMS = [("generic_intake", GenericIntakeForm), ]

# Fixed fee transactions
CS_FORMS = [("company_profile", CompanyProfileForm), ]
SF_FORMS = [("company_profile", FinancingProfileForm), ]
ES_FORMS = [("company_profile", FinancingProfileForm), ]
# CS_SF_FORMS = [("company_profile", CompanyAndFinancingProfileForm), ]


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
