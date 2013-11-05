# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.http import HttpResponseRedirect


from .forms import ManualLoginForm


class AjaxBaseTemplateMixin(object):
    """
    Mixin to provide "base_template" context variable
    which will use the ajax base-slim.html template or plain base.html template
    """
    def get_context_data(self, *args, **kwargs):
        context = super(AjaxBaseTemplateMixin, self).get_context_data(*args, **kwargs)

        context.update({
            'base_template': 'base-slim.html' if self.request.is_ajax() else 'base.html',
        })

        return context


class ManualLoginView(FormView):
    """
    Manual Login form to allow for us to login as users
    """
    form_class = ManualLoginForm
    template_name = 'default/login.html'

    def get_success_url(self):
        return '/'

    def get_form_kwargs(self):
        kwargs = super(ManualLoginView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs