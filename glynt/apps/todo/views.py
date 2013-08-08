# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

from glynt.apps.project.services.project_checklist import ProjectCheckListService
from glynt.apps.project.models import Project

from braces.views import JSONResponseMixin

from glynt.apps.project.models import Project
from .forms import CustomerToDoForm, AttachmentForm
from .models import ToDo, Attachment
from .services import CrocdocAttachmentService

import logging
logger = logging.getLogger('django.request')


class ProjectToDoView(ListView):
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

        self.project = get_object_or_404(Project, uuid=self.kwargs.get('uuid'))
        self.checklist_service = ProjectCheckListService(project=self.project)

        context.update({
            'project': self.project,
            'checklist': self.checklist_service,
            'counts': {
                'new': self.model.objects.new(project=self.project, user=self.request.user).count(),
                'open': self.model.objects.open(project=self.project, user=self.request.user).count(),
                'pending': self.model.objects.pending(project=self.project, user=self.request.user).count(),
                'resolved': self.model.objects.resolved(project=self.project, user=self.request.user).count(),
                'closed': self.model.objects.closed(project=self.project, user=self.request.user).count(),
            }
        })
        return context


class BaseToDoDetailMixin(SingleObjectMixin):
    model = ToDo

    def get_context_data(self, **kwargs):
        context = super(BaseToDoDetailMixin, self).get_context_data(**kwargs)
        context.update({
            'project': self.project_service.project,
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

            return obj


class ToDoDetailView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/todo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ToDoDetailView, self).get_context_data(**kwargs)
        context.update({
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
        #messages.success(self.request, 'Sucessfully updated this item. <a href="{href}">view</a>'.format(href=self.object.get_absolute_url()), extra_tags='safe')
        return super(ToDoEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating this item')
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

class ToDoAttachmentView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/attachments.html'


class ToDoAssignView(DetailView, BaseToDoDetailMixin):
    template_name = 'todo/assign.html'



class AttachmentSessionView(JSONResponseMixin, DetailView):
    """
    Obtain the appropriate crocdoc session to view a document
    view allows us to specify certain capabilities based on user class
    and type: https://github.com/crocodoc/crocodoc-python#session
    """
    model = Attachment
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    json_dumps_kwargs = {'indent': 3}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        service = CrocdocAttachmentService(attachment=self.object)

        params = {"user": {"name": request.user.get_full_name(), "id": request.user.pk}, "sidebar": 'auto', "editable": True, "admin": False, "downloadable": True, "copyprotected": False, "demo": False}
        session_key = service.session_key(**params)

        context_dict = {
            'session_key': session_key,
            'uuid': service.uuid,
            'view_url': service.view_url(),
        }

        return self.render_json_response(context_dict)