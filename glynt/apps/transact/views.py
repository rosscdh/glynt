# Create your views here.
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.contrib.formtools.wizard.views import SessionWizardView

from glynt.apps.transact.forms import PackagesForm, BasicInformationForm, CorporateAgentsForm, \
    InitialDirectorsForm, GeneralCapitalizationForm, FoundersForm, StockPlansForm, AboutCompanyBusinessForm, \
    IntellectualPropertyForm, EmployeesConsultantsForm


FORMS = [#("founders",FoundersForm),
         ("packages", PackagesForm),
         ("basic_information", BasicInformationForm),
         ("corporate_agents", CorporateAgentsForm),
         ("initial_directors",InitialDirectorsForm),
         ("general_capitalization", GeneralCapitalizationForm),
         ("founders",FoundersForm),
         ("stock_plans", StockPlansForm),
         ("about_company_business", AboutCompanyBusinessForm),
         ("intellectual_property", IntellectualPropertyForm),
         ("employees_consultants", EmployeesConsultantsForm)]

TEMPLATES = {"packages": "transact/packages_form.html",
             "basic_information": "transact/basic_information_form.html",
             "corporate_agents": "transact/corporate_agents_form.html",
             "initial_directors": "transact/initial_directors_form.html",
             "general_capitalization": "transact/general_capitalization_form.html",
             "founders": "transact/founders_form.html",
             "stock_plans": "transact/stock_plans_form.html",
             "about_company_business": "transact/about_company_business_form.html",
             "intellectual_property": "transact/intellectual_property_form.html",
             "employees_consultants": "transact/employees_consultants.html",

             #"other_agreements": "transact/other_agreements_form.html",
             #"existing_documentation": "transact/existing_documentation_form.html"}
            }


class PackagesWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/dashboard/matching')