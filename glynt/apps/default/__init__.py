# -*- coding: utf-8 -*-
"""
import ToDo signals here beacuse of problems with signals system
and certian email services @TODO sort out the email services
"""
from glynt.apps.todo.signals import (on_attachment_created,
                      on_attachment_deleted,
                      on_comment_created,
                      feedbackrequest_created,
                      feedbackrequest_status_change,
                      projectlawyer_assigned,
                      projectlawyer_deleted,
                      todo_item_status_change,
                      on_action_created,)