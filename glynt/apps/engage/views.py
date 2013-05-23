# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from glynt.apps.utils import _get_referer

from forms import EngageWriteMessageForm

import logging
logger = logging.getLogger('django.request')


class EngageWriteMessageView(FormView):
    form_class = EngageWriteMessageForm
    template_name = 'postman/write.html'
    auto_moderators = []

    def get_success_url(self):
        return _get_referer(self.request)

    def get_context_data(self, **kwargs):
        context = super(EngageWriteMessageView, self).get_context_data(**kwargs)
        context.update({
            'next_url': _get_referer(self.request),
            'to_user': self.to_user,
        })
        return context

    def get_form(self, form_class):
        """
        Inject the request into the form so we can extract the to and the from
        """
        self.to_user = get_object_or_404(User, username=self.kwargs.get('to'))
        kwargs = self.get_form_kwargs()

        # inject required vars into form
        kwargs.update({
            'to': self.to_user,
            'from': self.request.user,
            'request': self.request,
        })
        return form_class(**kwargs)

    def form_valid(self, form):
        is_successful = form.save(auto_moderators=self.auto_moderators)

        if is_successful:
            messages.success(self.request, _("Message successfully sent."), fail_silently=True)
        else:
            messages.warning(self.request, _("Message rejected for at least one recipient."), fail_silently=True)

        return super(EngageWriteMessageView, self).form_valid(form=form)