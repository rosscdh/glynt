from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, ProcessFormView
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from glynt.apps.document.models import Document


class SignupView(TemplateView):
    template_name = 'client/signup.html'


class LoginView(FormView):
    """ Primative login """
    template_name = 'client/login.html'
    success_url = '/'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        user = authenticate(username=request.POST.get('username',None), password=request.POST.get('password',None))

        if user is not None:
          if user.is_active:
            login(request, user)
            return self.form_valid(form)
          else:
            return self.form_invalid(form)
        else:
          return self.form_invalid(form)




class DashboardView(TemplateView):
    template_name = 'client/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['document_list'] = Document.objects.filter(owner=self.request.user)

        return context
