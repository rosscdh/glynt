# -*- coding: utf-8 -*-
from django.views.generic import ListView
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
                'new': self.model.objects.new(project=self.project, user=self.request.user).count(),
                'open': self.model.objects.open(project=self.project, user=self.request.user).count(),
                'closed': self.model.objects.closed(project=self.project, user=self.request.user).count(),
            }
        })
        return context


# class MyToDoListView(ListView):
#     model = ToDo
#     paginate_by = 1#10

#     def get_queryset(self):
#         """
#         Provide a list of todos for the current user
#         """
#         order_by = self.request.GET.get('order_by', '-id') # newest first

#         fltr = {
#             'status': self.request.GET.get('status', 1) # newest first
#         }

#         # filter by the current user always
#         # filter by the params passed in
#         queryset = self.model.objects.prefetch_related('user', 'project') \
#                         .filter(user=self.request.user) \
#                         .filter(**fltr)

#         return queryset.order_by(order_by)

#     def get_context_data(self, **kwargs):
#         context = super(MyToDoListView, self).get_context_data(**kwargs)
#         context.update({
#             'projects': Project.objects.for_user(user=self.request.user),
#             'counts': {
#                 'new': self.model.objects.new(user=self.request.user).count(),
#                 'open': self.model.objects.open(user=self.request.user).count(),
#                 'closed': self.model.objects.closed(user=self.request.user).count(),
#             }
#         })
#         return context


# class ToDoDetailView(ListView):
#     model = ToDo
