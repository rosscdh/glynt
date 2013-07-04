# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from glynt.apps.utils import AjaxableResponseMixin

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.customer.services import EnsureCustomerService
from glynt.apps.project.models import Project

from glynt.apps.transact.forms import PackagesForm

from bunches import CompanyEngageLawyerBunch

from signals import mark_project_notifications_as_read

import logging
logger = logging.getLogger('django.request')


class CreateProjectView(FormView):
    form_class = PackagesForm


class ProjectView(DetailView):
    model = Project

    def get_object(self, queryset=None):
        """"""
        queryset = self.get_queryset()
        # Next, try looking up by primary key.
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = queryset.select_related('startup','customer','lawyer','founder__user','lawyer__user').filter(slug=slug)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def render_to_response(self, context, **response_kwargs):
        """ @BUSINESSRULE if the viewing user is a founder, then mark their engagement notifications as read when they simply view the project """
        #if self.object.customer.user == self.request.user:
        mark_project_notifications_as_read(user=self.request.user, project=self.object)

        return super(ProjectView, self).render_to_response(context, **response_kwargs)


class CloseProjectView(AjaxableResponseMixin, UpdateView):
    model = Project
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            message = self.object.close(actioning_user=request.user)
        return self.render_to_json_response({'message': message, 'status': 200, 'instance': {'pk': self.object.pk, 'link': self.object.get_absolute_url()}})


class ReOpenProjectView(CloseProjectView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            message = self.object.reopen(actioning_user=request.user)
        return self.render_to_json_response({'message': message, 'status': 200, 'instance': {'pk': self.object.pk, 'link': self.object.get_absolute_url()}})


class MyProjectsView(ListView):
    model = Project
    def get_queryset(self):
        """"""
        user = self.request.user
        queryset = self.model.objects
        fltr = {}

        if user.profile.is_lawyer:
            fltr.update({'lawyer': user.lawyer_profile})
        elif user.profile.is_customer:
            fltr.update({'customer': user.customer_profile})
        else:
            """@BUSINESSRULE if they are neither a founder not a startup show them nothign
            @TODO this should all be in a manager """
            # is not a valid user type, show them nothing
            fltr.update({'pk': -1})

        return queryset.filter(**fltr)