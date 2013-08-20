# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.test.client import Client

from model_mommy import mommy

from actstream.models import Action
from glynt.apps.todo import TODO_STATUS


class TestToDoSignals(LiveServerTestCase):

    def setUp(self):
        self.client = Client()

        self.lawyer = mommy.make('lawyer.Lawyer')

        self.project = mommy.make('project.Project')
        mommy.make('project.ProjectLawyer', project=self.project, lawyer=self.lawyer)

        self.todo = mommy.make('todo.ToDo')


    def test_todo_item_status_change(self):
        self.assertTrue(self.todo.pk is not None)
        # print Action.objects.all()
        # assert False
        self.todo.status = TODO_STATUS.open
        self.todo.status.save()
