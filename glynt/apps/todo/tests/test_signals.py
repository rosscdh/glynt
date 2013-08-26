# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase
from django.test.client import Client

from glynt.casper import BaseLawyerCustomerProjectCaseMixin
from model_mommy import mommy

from actstream.models import Action
from glynt.apps.todo import TODO_STATUS, TODO_STATUS_ACTION


#from nose.tools import set_trace; set_trace()
class TestToDoSignals(BaseLawyerCustomerProjectCaseMixin):
    def test_todo_item_status_change(self):
        """
        Test that when a todo items status is changed
        1. a new action element is created
        1a. with the appropriate text as the event action
        """
        for ts in TODO_STATUS:
            #from nose.tools import set_trace; set_trace()
            Action.objects.all().delete() # remove all other action elements
            # there are no actions
            self.assertTrue(len(Action.objects.all()) == 0)

            self.todo.status = TODO_STATUS[ts]
            self.todo.save()

            actions = Action.objects.filter(action_object_object_id=self.todo.pk)

            self.assertTrue(len(actions) == 1) # we want only 1 to be created

            self.assertEqual(actions[0].data.get('event_action'), TODO_STATUS_ACTION[ts]) # must match the event type