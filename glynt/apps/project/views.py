# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, DetailView, UpdateView, CreateView
from django.views.generic.edit import DeletionMixin

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404

from notifications.models import Notification

from glynt.apps.utils import AjaxableResponseMixin

from glynt.apps.project.models import Project, ProjectLawyer
from glynt.apps.lawyer.models import Lawyer
from glynt.apps.project.forms import ContactUsForm, CreateProjectForm
from glynt.apps.project.services.ensure_project import EnsureProjectService

from glynt.apps.transact.models import Transaction

from . import PROJECT_LAWYER_STATUS
from .forms import ProjectCategoryForm

import json
import logging
logger = logging.getLogger('django.request')


class CreateProjectView(FormView):
    """ Start a new Project, by selecting 1 or more of the transactions """
    template_name = 'project/create/index.html'
    form_class = CreateProjectForm

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context.update({
            'contact_form': ContactUsForm(initial={}, request=self.request),
        })

        return context

    def save(self, transaction_types):
        customer = self.request.user.customer_profile
        company = customer.primary_company
        transactions = Transaction.objects.filter(slug__in=transaction_types)

        project_service = EnsureProjectService(customer=customer, company=company, transactions=transactions)
        project_service.process()

        self.project = project_service.project

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


class LawyerContactProjectView(ProjectView):
    """
    View to allow user to contact project lawyer
    """
    template_name = 'project/lawyer_contact.html'

    def mark_notifications(self, project_lawyer_join):
        """
        if the user has notifications then remove them here as weve seen them
        """
        objects = Notification.objects.filter(recipient=self.request.user,
                                    target_object_id=project_lawyer_join.project.pk,
                                    target_content_type=project_lawyer_join.project.content_type())  \

        if self.request.user.profile.is_customer:
            #delete only the comments specific to the lawyer being viewd
            objects = objects.filter(actor_object_id=project_lawyer_join.lawyer.user.pk,)

        objects.delete()

    def get_context_data(self, **kwargs):
        context = super(LawyerContactProjectView, self).get_context_data(**kwargs)

        lawyer = get_object_or_404(Lawyer.objects.prefetch_related('user'), user__username=self.kwargs.get('lawyer'))
        project_lawyer_join = ProjectLawyer.objects.get(project=self.object, lawyer=lawyer)

        self.mark_notifications(project_lawyer_join=project_lawyer_join)

        context.update({
            'PROJECT_LAWYER_STATUS': PROJECT_LAWYER_STATUS,
            'project_lawyer_join': project_lawyer_join,
            'primary_join': project_lawyer_join,
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


class ProjectCategoryView(AjaxableResponseMixin, CreateView, DeletionMixin):
    model = Project
    slug_field = 'uuid'
    form_class = ProjectCategoryForm
    template_name = 'project/project_category_form.html'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()

        try:
            delete_data = json.loads(self.request.read()) # expect a json structure
            self.object.delete_categories(delete_data.get('category'))
            self.object.save(update_fields=['data'])
            message = 'Deleted the Category "{category}" from project "{project}"'.format(category=delete_data.get('category', None), project=self.object)
        except:
            message = 'Could not delete category "{category}" for project "{project}"'.format(category=delete_data.get('category', None), project=self.object)
            logger.error(message)

        return self.render_to_json_response({'message': message,
                                             'status': 200, 
                                             'instance': {'pk': self.object.pk,
                                                          'link': self.object.get_absolute_url()
                                                         }
                                            })

    def form_invalid(self, form):
        return self.render_to_json_response({'message': json.dumps(form.errors),
                                             'status': 200, 
                                             'instance': {  'pk': self.object.pk,
                                                            'link': self.object.get_absolute_url(),
                                                            'category': {
                                                                'name': form.category,
                                                                'slug': form.category_slug
                                                            }
                                                         }
                                            })

    def form_valid(self, form):
        form.save()
        return self.render_to_json_response({'message': form.message,
                                             'status': 200, 
                                             'instance': {  'pk': self.object.pk,
                                                            'link': self.object.get_absolute_url(),
                                                            'category': {
                                                                'name': form.category,
                                                                'slug': form.category_slug
                                                            }
                                                         }
                                            })

    def get_category(self):
        return self.request.GET.get('category', None)

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({
            'category': self.get_category()
        })
        return initial

    def get_form_kwargs(self):
        self.object = self.get_object()

        kwargs = super(ProjectCategoryView, self).get_form_kwargs()

        kwargs.update({
            'project_uuid': self.object.uuid,
            'original_category': self.get_category()
        })
        return kwargs