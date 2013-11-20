# -*- coding: utf-8 -*-
"""
"""
from glynt.casper import BaseLawyerCustomerProjectCaseMixin, for_all_methods, glynt_mock_http_requests
from glynt.apps.todo import TODO_STATUS, FEEDBACK_STATUS
from model_mommy import mommy

import httpretty


@for_all_methods(glynt_mock_http_requests)
class FeedbackRequestManagerTest(BaseLawyerCustomerProjectCaseMixin):
    def setUp(self):
        super(FeedbackRequestManagerTest, self).setUp()

        self.todo = mommy.make('todo.ToDo', status=TODO_STATUS.open, project=self.project, user=self.lawyer_user, category='General')
        self.attachment = mommy.make('todo.Attachment', project=self.project, todo=self.todo, uploaded_by=self.customer_user)

        self.feedback_request = mommy.make('todo.FeedbackRequest', status=FEEDBACK_STATUS.open, attachment=self.attachment, assigned_by=self.customer_user, assigned_to=(self.lawyer_user,), comment='What are your thoughts on this test file with ümlauts')

    def test_close_todo_sets_feedbackrequest_to_canceled(self):
        """
        When the todo item gets closed
        then all open FeedbackRequests should be set to cancelled and have a closed message
        @MOCK crocdoc
        """
        httpretty.register_uri(httpretty.POST, "https://crocodoc.com/api/v2/document/upload",
                       body='{"success": true, "uuid": "123-test-123-uuid"}',
                       status=200,
                       content_type='text/json')

        self.assertTrue(self.todo.pk is not None)
        self.assertEqual(self.todo.status, TODO_STATUS.pending) # because we have assigned a feedback request to it
        self.assertEqual(self.feedback_request.status, FEEDBACK_STATUS.open)

        self.todo.status = TODO_STATUS.closed
        self.todo.save()
        
        # reload the object
        self.feedback_request = self.feedback_request.__class__.objects.get(pk=self.feedback_request.pk)

        self.assertEqual(self.todo.status, TODO_STATUS.closed)
        self.assertEqual(self.feedback_request.status, FEEDBACK_STATUS.cancelled)
        self.assertEqual(self.feedback_request.comment, 'Todo instance was set to closed. All open Feedback requests were therefor cancelled')