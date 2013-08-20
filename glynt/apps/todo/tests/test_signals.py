# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.test.client import Client

from model_mommy import mommy

from actstream.models import Action
from glynt.apps.todo import TODO_STATUS


class TestToDoSignals(LiveServerTestCase):
    fixtures = ['test_cities']

    def setUp(self):
        self.client = Client()

        self.user = mommy.make('auth.User', first_name='FirstName', last_name='Surname', email='test@lawpal.com')
        self.customer = mommy.make('customer.Customer', user=self.user)
        self.lawyer = mommy.make('lawyer.Lawyer')

        self.project = mommy.make('project.Project', customer=self.customer)
        mommy.make('project.ProjectLawyer', project=self.project, lawyer=self.lawyer)

        self.todo = mommy.make('todo.ToDo', user=self.user, project=self.project)

    def test_todo_item_status_change(self):
        """ Should use mocks here """

        self.assertTrue(self.todo.pk is not None)

        # there are no actions
        self.assertTrue(len(Action.objects.all()) == 0)

        self.todo.status = TODO_STATUS.pending
        self.todo.save()

        self.assertTrue(len(Action.objects.filter(action_object_object_id=self.todo.pk)) == 1)