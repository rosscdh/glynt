from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User


from forms import ConfirmLoginDetailsForm, SignupForm, AuthenticationForm

import logging
logger = logging.getLogger('django.request')


class ConfirmLoginDetailsView(UpdateView):
    model = User
    slug_field = 'username'
    template_name = 'client/confirm_login_details.html'
    form_class = ConfirmLoginDetailsForm

    def get_success_url(self):
        return reverse('public:homepage')

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return form_class(**kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        slug_field = self.get_slug_field()
        queryset = User.objects.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_initial(self):
        user = self.request.user
        return {
            'username': user.username,
            'email': user.email,
            'password': user.password,
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            messages.info(request, _('Welcome, you have successfully signed up.'))
            form.save()
            logger.info('User %s has confirmed their account' % request.user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SignupView(FormView):
    template_name = 'userena/signup_form.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('client:dashboard')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            messages.info(request, _('Welcome, you have successfully signed up. Please remember to check your email and activate your account once you recieve our welcome email.'))
            user = form.save()
            logger.info('A user has signed up %s' % user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LoginView(FormView):
    """ Primative login """
    template_name = 'client/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('client:dashboard')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        user = authenticate(username=request.POST.get('username', None), password=request.POST.get('password', None))

        if user is None:
            logger.warn('Incorrect login attempt user: %s' % request.POST.get('username', None))
        else:
            if user.is_active:
                login(request, user)
                if request.GET.get('next') is not None:
                    self.success_url = request.GET.get('next')
                messages.success(request, _('Welcome, you have successfully logged in.'))

                logger.info('LoggedIn user: %s' % user)

                return self.form_valid(form)
            else:
                messages.info(request, _('Sorry, but your Account has yet to be acivated.'))
                logger.info('Inactive login attempt user: %s' % request.POST.get('username', None))

        return self.form_invalid(form)


class DashboardView(TemplateView):
    template_name = 'client/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['csrf_raw_token'] = get_token(self.request)

        return context
