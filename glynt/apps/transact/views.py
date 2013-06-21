# Create your views here.
from django.contrib.formtools.wizard.views import CookieWizardView
from django.http import HttpResponseRedirect

from glynt.apps.transact.forms import PackagesForm, BasicInformationForm

FORMS = [("packages", PackagesForm),
         ('basic_information', BasicInformationForm)]

TEMPLATES = {"packages": "transact/packages_form.html",
             "basic_information": "transact/basic_information.html"}


class PackagesWizard(CookieWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/')