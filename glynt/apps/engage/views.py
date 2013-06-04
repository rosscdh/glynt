# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.views.generic import FormView, DetailView, ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from postman.api import pm_write

from glynt.apps.utils import _get_referer, AjaxableResponseMixin

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.startup.services import EnsureFounderService
from bunches import StartupEngageLawyerBunch

from forms import EngageWriteMessageForm, EngageStartupLawyerForm
from models import Engagement

import logging
logger = logging.getLogger('django.request')


class EngageWriteMessageView(FormView, AjaxableResponseMixin):
    form_class = EngageWriteMessageForm
    template_name = 'postman/write.html'
    auto_moderators = []


    def get_context_data(self, **kwargs):
        """ 
        set context variables for form redirection
        """
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
            msg = _("Message successfully sent.")
            status = 200
        else:
            msg = _("Message could not be sent.")
            status = 500

        return self.render_to_json_response({'message': unicode(msg), 'status': status})

    def form_invalid(self, form):
        logger.error('EngageWriteMessageView.form_invalid %s' % ', '.join(form.errors))
        return self.render_to_json_response({'message': '<br/>'.join(form.errors), 'status': 500})



class StartupEngageLawyerView(AjaxableResponseMixin, FormView):
    form_class = EngageStartupLawyerForm
    template_name = 'engage/startup-lawyer.html'

    def get_form(self, form_class):
        """
        """
        self.lawyer = get_object_or_404(Lawyer, pk=self.kwargs.get('lawyer_pk'))

        self.engagement = Engagement.objects.founder_lawyer_engagement(founder=self.request.user.founder_profile, lawyer=self.lawyer)

        #self.engagement = 
        kwargs = self.get_form_kwargs()

        founder_service = EnsureFounderService(user=self.request.user)
        founder = founder_service.process()

        initial = StartupEngageLawyerBunch(founder=founder)

        if self.engagement is not None:
            initial.update({
                'engagement_statement': self.engagement.engagement_statement,
                'engage_for_general': self.engagement.data.get('engage_for_general',False),
                'engage_for_incorporation': self.engagement.data.get('engage_for_incorporation',False),
                'engage_for_ip': self.engagement.data.get('engage_for_ip',False),
                'engage_for_employment': self.engagement.data.get('engage_for_employment',False),
                'engage_for_cofounders': self.engagement.data.get('engage_for_cofounders',False),
                'engage_for_fundraise': self.engagement.data.get('engage_for_fundraise',False),
            })

        kwargs.update({
            'request': self.request,
            'lawyer': self.lawyer,
            'initial': initial,

        })
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        """ """
        context = super(StartupEngageLawyerView, self).get_context_data(**kwargs)
        context.update({
            'lawyer': self.lawyer,
            'engagement': self.engagement,
        })
        return context

    def form_valid(self, form):
        engagement = form.save()

        if engagement.pk:
            msg = _("Message of Engagement successfully sent. <a href=\"%s\">Click here to view</a>" % engagement.get_absolute_url())
            status = 200
        else:
            msg = _("Message of Engagement could not be sent.")
            status = 500

        return self.render_to_json_response({'message': unicode(msg), 'status': status, 'instance': {'pk': engagement.pk, 'link': engagement.get_absolute_url()}})


class EngagementView(DetailView):
    model = Engagement

    def get_object(self, queryset=None):
        """"""
        queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.select_related('startup','founder','lawyer','founder__user','lawyer__user').filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class MyEngagementsView(ListView):
    model = Engagement

    def get_queryset(self):
        """"""
        user = self.request.user
        queryset = self.model.objects
        fltr = {}
        if user.profile.is_lawyer:
            fltr.update({'lawyer': user.lawyer_profile})
        #elif user.profile.is_startup:
        else:
            fltr.update({'founder': user.founder_profile})

        return queryset.filter(**fltr)