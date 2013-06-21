# Create your views here.
from django.contrib.formtools.wizard.views import CookieWizardView
from django.http import HttpResponseRedirect

from glynt.apps.transact.forms import PackagesForm, BasicInformationForm, OtherAgreementsForm

FORMS = [("packages", PackagesForm),
         ('basic_information', BasicInformationForm),
         ('other_agreements', OtherAgreementsForm)]

TEMPLATES = {"packages": "transact/packages_form.html",
             "basic_information": "transact/basic_information_form.html",
             "other_agreements": "transact/other_agreements_form.html"}


class PackagesWizard(CookieWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/')