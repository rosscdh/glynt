# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin

from glynt.apps.rulez import RulezMixin
from glynt.apps.project.services.project_checklist import ProjectCheckListService
from glynt.apps.project.models import Project


from . import TODO_STATUS, FEEDBACK_STATUS
from .forms import CustomerToDoForm, AttachmentForm, FeedbackRequestForm
from .models import ToDo, Attachment, FeedbackRequest
from .services import CrocdocAttachmentService

import logging
logger = logging.getLogger('django.request')


class ToDoCountMixin(object):
    def todo_counts(self, qs_objects, project=None, **kwargs):
        project = project if project is not None else self.project

        awaiting_feedback_from_user = FeedbackRequest.objects.prefetch_related('attachment', 'attachment__project').filter(attachment__project=project, assigned_to=self.request.user).count()

        counts = {'counts': {
                    'new': qs_objects.new(project=project, **kwargs).count(),
                    'open': qs_objects.open(project=project, **kwargs).count(),
                    'pending': qs_objects.pending(project=project, **kwargs).count(),
                    'awaiting_feedback_from_user': awaiting_feedback_from_user,
                    'closed': qs_objects.closed(project=project, **kwargs).count(),

                    'total': 0,
                    }
                }
        counts['counts']['total'] = counts['counts']['new'] + counts['counts']['open'] + counts['counts']['pending']

        return counts


class ProjectToDoView(RulezMixin, ToDoCountMixin, ListView):
    model = ToDo
    paginate_by = 1  # 10

    def get_queryset(self):
        """
        Provide a list of todos for the current user
        """
        order_by = self.request.GET.get('order_by', '-id')  # newest first

        fltr = {
            'project': Project.objects.get(uuid=self.kwargs.get('uuid')),
        }

        # filter by the current user always
        # & filter by the params passed in
        queryset = self.model.objects.prefetch_related('user', 'project') \
                                     .filter(**fltr)

        return queryset.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(ProjectToDoView, self).get_context_data(**kwargs)

        user_profile = self.request.user.profile

        self.project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))
        self.can_read(self.project)

        self.checklist_service = ProjectCheckListService(project=self.project)
        self.feedback_requests = self.checklist_service.feedbackrequests_by_user_as_json(user=self.request.user)

        context.update({
            'project': self.project,
            'checklist': self.checklist_service,
            'feedback_requests': self.feedback_requests,
            'is_lawyer': user_profile.is_lawyer,
            'is_customer': user_profile.is_customer,
        })
        # append counts
        context.update(self.todo_counts(qs_objects=self.model.objects))

        context['counts']['total'] = context['counts']['new'] + context['counts']['open'] + context['counts']['pending']
        return context


class BaseToDoDetailMixin(RulezMixin, SingleObjectMixin):
    model = ToDo

    def get_context_data(self, **kwargs):
        context = super(BaseToDoDetailMixin, self).get_context_data(**kwargs)
        context.update({
            'project': self.project_service.project,
            'feedback_form': FeedbackRequestForm(),
        })
        return context

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        slug = self.kwargs.get(self.slug_url_kwarg, 'slug')

        self.project = get_object_or_404(Project, uuid=self.kwargs.get('project_uuid'))
        self.project_service = ProjectCheckListService(project=self.project)

        self.navigation_items = self.project_service.navigation_items_object(slug=slug)

        if self.navigation_items.current is None:
            # does nto seem to exist need to log and error
            logger.error('ToDo item does not exist in categories navigation_items but it should! {slug}, navigation_items: {navigation_items}'.format(slug=slug, navigation_items=self.navigation_items))
            return None
        else:
            obj, is_new = self.model.objects.get_or_create(slug=slug, project=self.project)
            nav_item = self.navigation_items.current
            if is_new and nav_item:
                obj.name = nav_item.name
                obj.category = nav_item.category
                obj.description = nav_item.description
                obj.status = nav_item.status
                obj.data = nav_item
                obj.save()

            self.can_read(obj)

            return obj


class ToDoDetailView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/todo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoDetailView, self).get_context_data(**kwargs)
        context.update({
            'TODO_STATUS': TODO_STATUS,
            'attachment_form': AttachmentForm(initial={'project': self.project.pk, 'todo': self.object.pk}),
            'back_and_forth': self.navigation_items,
        })
        return context


class ToDoDiscussionView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/discussion.html'


class ToDoEditView(UpdateView, BaseToDoDetailMixin, ModelFormMixin):
    template_name = 'todo/todo_form.html'
    form_class = CustomerToDoForm

    def get_success_url(self):
        return self.project.get_checklist_absolute_url()

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ToDoEditView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'project_service': self.project_service,
            'project_uuid': self.kwargs.get('project_uuid'), 
            'slug': self.kwargs.get('slug'), 
        })
        return kwargs

    def form_valid(self, form):
        return super(ToDoEditView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ToDoEditView, self).form_valid(form)


class ToDoCreateView(ToDoEditView):
    template_name = 'todo/todo_form.html'
    form_class = CustomerToDoForm

    def get_form_kwargs(self):
        kwargs = super(ToDoCreateView, self).get_form_kwargs()
        kwargs.update({
            'is_create': True,
        })
        return kwargs


"""
Attachment Views
"""
class CrocdocAttachmentSessionContextMixin(View):
    def get_context_data(self, **kwargs):
        context = super(CrocdocAttachmentSessionContextMixin, self).get_context_data(**kwargs)
        service = CrocdocAttachmentService(attachment=self.object)

        crocdoc_params = {
                "user": { "name": self.request.user.get_full_name(), 
                "id": self.request.user.pk
            }, 
            "sidebar": 'auto', 
            "editable": True, 
            "admin": False, 
            "downloadable": True, 
            "copyprotected": False, 
            "demo": False
        }

        context.update({
            'session_key': service.session_key(**crocdoc_params),
            'uuid': service.uuid,
            'view_url': service.view_url(),
        })
        return context


class AttachmentView(CrocdocAttachmentSessionContextMixin, DetailView):
    template_name = 'todo/attachment.html'
    model = Attachment

    @property
    def opposite_user(self):
        try:
            return self.object.project.get_primary_lawyer().user if self.request.user.profile.is_customer else self.object.project.customer.user
        except AttributeError:
            return None

    def get_context_data(self, **kwargs):
        context = super(AttachmentView, self).get_context_data(**kwargs)
        context.update({
            'has_lawyer': self.object.project.has_lawyer,
            'is_lawyer': self.request.user.profile.is_lawyer,
            'feedback_requests': self.object.feedbackrequest_set.open(),
            'opposite_user': self.opposite_user,
            'FEEDBACK_STATUS': FEEDBACK_STATUS,
        })
        return context
