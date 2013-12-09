# -*- coding: UTF-8 -*-
from glynt.apps.utils import get_namedtuple_choices


TODO_STATUS = get_namedtuple_choices('TODO_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'pending', 'Pending'),
    (3, 'resolved', 'Resolved'),
    (4, 'closed', 'Closed'),
))


TODO_STATUS_ACTION = {
    TODO_STATUS.new: 'set as New',
    TODO_STATUS.open: 'Opened',
    TODO_STATUS.pending: 'set as Pending',
    TODO_STATUS.resolved: 'Resolved',
    TODO_STATUS.closed: 'Closed',
}


FEEDBACK_STATUS = get_namedtuple_choices('FEEDBACK_STATUS', (
    (0, 'open', 'Open'),
    (1, 'acknowledged', 'Acknowldeged'),
    (2, 'responded', 'Responded'),
    (3, 'closed', 'Closed'),
    (4, 'cancelled', 'Cancelled') # for when a lawyer closes a todo that has open feedback-requests
))


"""
import signals
"""
from .signals import (on_attachment_created,
                      on_attachment_deleted,
                      on_comment_created,
                      feedbackrequest_created,
                      feedbackrequest_status_change,
                      projectlawyer_assigned,
                      projectlawyer_deleted,
                      todo_item_status_change,
                      on_action_created,)
