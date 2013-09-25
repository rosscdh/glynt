# -*- coding: UTF-8 -*-
from bunch import Bunch
from glynt.apps.todo.models import FeedbackRequest


class UserFeedbackRequestMixin(object):
    def feedbackrequests_by_user(self, user):
        return FeedbackRequest.objects.open(assigned_to=user)

    def feedbackrequests_by_user_as_json(self, user):
        """
        Return a set of attachment feedback requests
        grouped by todo.slug
        """
        json_response = {}
        for f in self.feedbackrequests_by_user(user=user):
            json_response[f.attachment.todo.slug] = json_response.get(f.attachment.todo.slug, [])
            json_response[f.attachment.todo.slug].append(Bunch(todo_slug=f.attachment.todo.slug))

        return json_response
