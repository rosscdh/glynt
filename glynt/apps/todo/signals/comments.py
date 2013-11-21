# -*- coding: utf-8 -*-
"""
Comment Events
"""
from django.dispatch import receiver
from django.db.models.signals import post_save

from actstream import action
from notifications import notify
from threadedcomments.models import ThreadedComment

from glynt.apps.todo.services import ToDoStatusService

from glynt.apps.todo.signals import get_todo_info_object

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=ThreadedComment, dispatch_uid='todo.comment.created')
def on_comment_created(sender, **kwargs):
    """
    Handle Creation of attachments
    @TODO: This needs to be abstracted!
    @CODESMELL
    """
    if sender.__class__.__name__ != 'LogEntry':
        send = False
        is_new = kwargs.get('created', False)
        comment = kwargs.get('instance')
        extra = {}

        if comment and is_new:
            content_object_type = comment.content_object.__class__.__name__

            logger.debug('New Comment on object type: {content_object_type}'.format(content_object_type=content_object_type))

            # If its a comment on a ToDo Object
            if content_object_type == 'ToDo':
                send = True
                target = todo = comment.content_object
                event = 'todo.comment.created'
                verb = '{name} commented on checklist item {todo} for {project}'.format(name=comment.user.get_full_name(), project=todo.project, todo=todo.name)

                # update the ToDo Status as its been interacted with
                todostatus_service = ToDoStatusService(todo_item=todo)
                todostatus_service.process()

                # append the todo instance object
                extra.update(get_todo_info_object(todo=todo))

            elif content_object_type == 'Project':
                send = True
                target = project = comment.content_object
                event = 'project.comment.created'
                verb = '{name} commented on the {project} project'.format(name=comment.user.get_full_name(), project=project)
                extra.update({
                    'url': comment.absolute_deeplink_url()  # append url to the comment deeplink
                })

            elif content_object_type == 'ProjectLawyer':
                send = True
                target = comment_target = comment.content_object
                event = 'project.lawyer_engage.comment.created'
                verb = '{name} commented on the Lawyer Engagement conversation for {project}'.format(name=comment.user.get_full_name(), project=comment_target.project)

                # notify the lawyer (used for discussion counts)
                if comment.user.profile.is_customer:
                    recipient = comment.content_object.lawyer.user
                else:
                    recipient = comment.content_object.project.customer.user
                # send notification
                notify.send(comment.user, recipient=recipient, verb=u'added to discussion', action_object=comment_target.project,
                    description=comment.comment, target=comment_target.project, project_action='added_discussion_item', project_pk=comment_target.project.pk, creating_user_pk=comment.user.pk)

        if send is True:
            logger.debug('send action: {event} {verb} content: {content}'.format(event=event, verb=verb, content=comment.comment))
            action.send(comment.user,
                        verb=verb,
                        action_object=comment,
                        target=target,
                        content=comment.comment,
                        event=event,
                        **extra)