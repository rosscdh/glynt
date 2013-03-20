# -*- coding: UTF-8 -*-
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from forms import CreateLawyerFirmForm


class CreateFirmView(FormView):
    form_class = CreateLawyerFirmForm
    template_name = 'firm/create.html'

    def get_success_url(self):
        return reverse('firms:create')

    def form_valid(self, form):
        messages.success(self.request, 'Thanks, you created a new Lawyer')
        form.save()
        return HttpResponseRedirect(self.get_success_url())