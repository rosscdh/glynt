# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from glynt.apps.todo.models import ToDo


class MyToDoListView(ListView):
    model = ToDo
    paginate_by = 10

    def get_queryset(self):
        """
        Provide a list of todos for the current user
        """
        queryset = self.model.objects.filter(user=self.request.user).all()
        return queryset


class ToDoDetailView(ListView):
    model = ToDo