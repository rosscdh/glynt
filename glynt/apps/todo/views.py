# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from glynt.apps.project.services.project_checklist import ProjectCheckListService
from glynt.apps.project.models import Project
from .models import ToDo


class ProjectToDoView(ListView):
    model = ToDo
    paginate_by = 1  # 10

    def get_queryset(self):
        """
        Provide a list of todos for the current user
        """
        order_by = self.request.GET.get('order_by', '-id')  # newest first

        fltr = {
            'status': self.request.GET.get('status', 1)  # newest first
        }

        # filter by the current user always
        # filter by the params passed in
        queryset = self.model.objects.prefetch_related('user', 'project') \
                                     .filter(user=self.request.user) \
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
                'new': self.model.objects.unassigned(project=self.project, user=self.request.user).count(),
                'open': self.model.objects.assigned(project=self.project, user=self.request.user).count(),
                'closed': self.model.objects.closed(project=self.project, user=self.request.user).count(),
            }
        })
        return context


class BaseToDoDetailView(DetailView):
    model = ToDo

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        self.project = get_object_or_404(Project, uuid=self.kwargs.get('project_uuid'))
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        obj = self.model.objects.get_or_create(slug=slug, project=self.project)

        return obj


class ToDoDetailView(BaseToDoDetailView):
    template_name = 'todo/todo_detail.html'


class ToDoCommentView(BaseToDoDetailView):
    template_name = 'todo/discussion.html'


class ToDoEditView(BaseToDoDetailView):
    template_name = 'todo/todo_form.html'


class ToDoAttachmentView(BaseToDoDetailView):
    template_name = 'todo/attachments.html'


class ToDoAssignView(BaseToDoDetailView):
    template_name = 'todo/assign.html'
