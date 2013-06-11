# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from glynt.apps.utils import AjaxableResponseMixin

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.startup.services import EnsureFounderService
from glynt.apps.engage.models import Engagement

from bunches import StartupEngageLawyerBunch

from forms import EngageStartupLawyerForm
from signals import mark_engagement_notifications_as_read

import logging
logger = logging.getLogger('django.request')


class StartupEngageLawyerView(AjaxableResponseMixin, FormView):
    form_class = EngageStartupLawyerForm
    template_name = 'engage/startup-lawyer.html'

    def get_form(self, form_class):
        """
        """
        self.lawyer = get_object_or_404(Lawyer, pk=self.kwargs.get('lawyer_pk'))

        self.engagement = Engagement.objects.historic(founder=self.request.user.founder_profile, lawyer=self.lawyer)

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
            msg = _("Thanks. That Lawyer has been contacted. <a href=\"%s\">Check here for updates</a>" % engagement.get_absolute_url())
            status = 200
        else:
            msg = _("Sorry, contact could not be made wih this Lawyer.")
            status = 500

        return self.render_to_json_response({'message': unicode(msg), 'status': status, 'instance': {'pk': engagement.pk, 'link': engagement.get_absolute_url()}})


class EngagementView(DetailView):
    model = Engagement

    def get_object(self, queryset=None):
        """"""
        queryset = self.get_queryset()
        # Next, try looking up by primary key.
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = queryset.select_related('startup','founder','lawyer','founder__user','lawyer__user').filter(slug=slug)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def render_to_response(self, context, **response_kwargs):
        """ @BUSINESSRULE if the viewing user is a founder, then mark their engagement notifications as read when they simply view the engagement """
        #if self.object.founder.user == self.request.user:
        mark_engagement_notifications_as_read(user=self.request.user, engagement=self.object)

        return super(EngagementView, self).render_to_response(context, **response_kwargs)


class CloseEngagementView(AjaxableResponseMixin, UpdateView):
    model = Engagement
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            message = self.object.close(actioning_user=request.user)
        return self.render_to_json_response({'message': message, 'status': 200, 'instance': {'pk': self.object.pk, 'link': self.object.get_absolute_url()}})


class ReOpenEngagementView(CloseEngagementView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            message = self.object.reopen(actioning_user=request.user)
        return self.render_to_json_response({'message': message, 'status': 200, 'instance': {'pk': self.object.pk, 'link': self.object.get_absolute_url()}})


class MyEngagementsView(ListView):
    model = Engagement
    def get_queryset(self):
        """"""
        user = self.request.user
        queryset = self.model.objects
        fltr = {}

        if user.profile.is_lawyer:
            fltr.update({'lawyer': user.lawyer_profile})
        elif user.profile.is_founder:
            fltr.update({'founder': user.founder_profile})
        else:
            """@BUSINESSRULE if they are neither a founder not a startup show them nothign
            @TODO this should all be in a manager """
            # is not a valid user type, show them nothing
            fltr.update({'pk': -1})

        return queryset.filter(**fltr)