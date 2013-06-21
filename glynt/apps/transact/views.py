# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

from glynt.apps.transact.forms import PackagesForm, BasicInformationForm, OtherAgreementsForm, ExistingDocumentationForm

FORMS = [("packages", PackagesForm),
         ('basic_information', BasicInformationForm),
         ('other_agreements', OtherAgreementsForm),
         ('existing_documentation', ExistingDocumentationForm)]

TEMPLATES = {"packages": "transact/packages_form.html",
             "basic_information": "transact/basic_information_form.html",
             "other_agreements": "transact/other_agreements_form.html",
             "existing_documentation": "transact/existing_documentation_form.html"}


class PackagesWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/dashboard/matching')