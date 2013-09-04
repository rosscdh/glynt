# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, DetailView, ListView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404

from glynt.apps.utils import AjaxableResponseMixin

from glynt.apps.project.models import Project, ProjectLawyer
from glynt.apps.lawyer.models import Lawyer
from glynt.apps.project.forms import CreateProjectForm
from glynt.apps.project.services.ensure_project import EnsureProjectService

from glynt.apps.project.services.ensure_project import PROJECT_CREATED

from glynt.apps.client.services import EnsureUserHasCompletedIntakeProcess

from glynt.apps.transact.models import Transaction


from .signals import mark_project_notifications_as_read
from . import PROJECT_LAWYER_STATUS

import logging
logger = logging.getLogger('django.request')


class CreateProjectView(FormView):
    """ Start a new Project, by selecting 1 or more of the transactions """
    template_name = 'project/create.html'
    form_class = CreateProjectForm

    def save(self, transaction_types):
        customer = self.request.user.customer_profile
        company = customer.primary_company
        transactions = Transaction.objects.filter(slug__in=transaction_types)

        project_service = EnsureProjectService(customer=customer, company=company, transactions=transactions)
        project_service.process()

        self.project = project_service.project

        # only perform this if we have no other transaction types to manage
        if len(transaction_types) == 0:
            PROJECT_CREATED.send(sender=project_service, instance=project_service.project, created=project_service.is_new)

        return self.project

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        transaction_types = form.cleaned_data.get('transaction_type', '').split(',')

        if transaction_types is False:
            logger.error('transaction_types was not set in CreateProjectView')
            messages.error(self.request, _('Sorry, but we could not determine which transaction type you selected. Please try again.'))
            self.success_url = reverse('project:create')

        # intake = EnsureUserHasCompletedIntakeProcess(user=self.request.user)
        # if intake.is_complete() is False:
        #     if u'INTAKE' not in transaction_types:
        #         transaction_types.insert(0, u'INTAKE')

        project = self.save(transaction_types=transaction_types)

        self.success_url = reverse('transact:builder', kwargs={'project_uuid': project.uuid, 'tx_range': ','.join(transaction_types), 'step': 1})

        return super(CreateProjectView, self).form_valid(form)


class ProjectView(DetailView):
    model = Project

    def get_object(self, queryset=None):
        """"""
        queryset = self.get_queryset()
        # Next, try looking up by primary key.
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        queryset = queryset.select_related('startup', 'customer', 'lawyers', 'founder__user', 'lawyer__user').filter(uuid=slug)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    # def render_to_response(self, context, **response_kwargs):
    #     """ @BUSINESSRULE if the viewing user is a founder, then mark their engagement notifications as read when they simply view the project """
    #     #if self.object.customer.user == self.request.user:
    #     mark_project_notifications_as_read(user=self.request.user, project=self.object)

    #     return super(ProjectView, self).render_to_response(context, **response_kwargs)


class LawyerContactProjectView(ProjectView):
    """
    View to allow user to contact project lawyer
    """
    template_name = 'project/lawyer_contact.html'
    def get_context_data(self, **kwargs):
        context = super(LawyerContactProjectView, self).get_context_data(**kwargs)

        lawyer = get_object_or_404(Lawyer.objects.prefetch_related('user'), user__username=self.kwargs.get('lawyer'))

        context.update({
            'PROJECT_LAWYER_STATUS': PROJECT_LAWYER_STATUS,
            'project_lawyer_join': ProjectLawyer.objects.get(project=self.object, lawyer=self.object.primary_lawyer),
            'lawyer': lawyer,
        })

        return context


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
