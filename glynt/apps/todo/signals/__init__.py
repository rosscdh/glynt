# -*- coding: utf-8 -*-

def get_todo_info_object(todo):
    return {
        'instance': {
            'pk': todo.pk,
            'slug': todo.slug,
            'name': todo.name,
            'category': todo.category,
            'project': {'pk': todo.project.pk},
            'display_status': todo.display_status,
            'status': todo.status,
            'is_deleted': todo.is_deleted,
            'uri': todo.get_absolute_url(),
        }
    }

from .actions import on_action_created
from .attachments import on_attachment_created, on_attachment_deleted
from .comments import on_comment_created
from .feedback_requests import feedbackrequest_created, feedbackrequest_status_change
from .project_lawyer import projectlawyer_assigned, projectlawyer_deleted
from .todos import todo_item_crud, todo_item_status_change
