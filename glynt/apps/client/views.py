from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView, ProcessFormView
from django.views.generic.detail import BaseDetailView
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login


from socialregistration.contrib.facebook_js.models import FacebookProfile
from glynt.apps.document.models import Document
from forms import SignupForm, AuthenticationForm


class SignupView(FormView):
    template_name = 'userena/signup_form.html'
    success_url = '/'
    form_class = SignupForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        user = authenticate(username=request.POST.get('username',None), password=request.POST.get('password',None))

        if user is not None:
          if user.is_active:
            login(request, user)
            return self.form_valid(form)
          else:
            return self.form_invalid(form)
        else:
          return self.form_invalid(form)


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


class HasLocalFacebookAccountView(BaseDetailView):
    """ Used to evaluate if the facebook user exists in our system or not @TODO move to socialregistration? """
    def get_queryset(self):
        return FacebookProfile.objects.all()

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        uid = self.request.GET.get('uid', None)

        if uid is None:
            raise Http404("Facebook uid does not exist")
        
        try:
            obj = queryset.get(uid=uid)
        except FacebookProfile.DoesNotExist:
            raise Http404("Facebook %(uid)s could not be found" % {'uid': uid})
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return HttpResponse('[{"exists":true, "is_authenticated": %s}]' %(str(request.user.is_authenticated()).lower()), status=200)


class DashboardView(TemplateView):
    template_name = 'client/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['document_list'] = Document.objects.filter(owner=self.request.user)

        return context
