# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver

from notifications import notify

from notifications.models import Notification

from glynt.apps.project.utils import PROJECT_CONTENT_TYPE

from glynt.apps.project.services.email import SendNewProjectEmailsService
from glynt.apps.project.services.project_checklist import ProjectCheckListService
from glynt.apps.project.services.ensure_project import PROJECT_CREATED

import logging
logger = logging.getLogger('django.request')


@receiver(PROJECT_CREATED, dispatch_uid='project.on_project_created')
def on_project_created(sender, **kwargs):
    """
    Handle new Project
    """
    is_new = kwargs.get('created')
    project = kwargs.get('instance')

    if project:
        user = project.customer.user
        comment = u'{user} created this Project'.format(user=user.get_full_name())
        logger.debug(comment)
        # send notification
        notify.send(user, recipient=user, verb=u'created', action_object=project,
                    description=comment, target=project, project_action='created_project', project_pk=project.pk, creating_user_pk=user.pk)

        checklist_service = ProjectCheckListService(project=project)
        checklist_service.bulk_create()

        send = SendNewProjectEmailsService(project=project, sender=user)
        send.process()


def mark_project_notifications_as_read(user, project):
    """ used to mark the passed in users notifications for a specific project as read (can be either a lawyer or a customer) """
    logger.debug('marking unred notifications as read for user: %s and project: %s'%(user, project.pk))
    Notification.objects.filter(recipient=user, target_object_id=project.pk, unread=True, target_content_type=PROJECT_CONTENT_TYPE).mark_all_as_read()


# @receiver(post_save, sender=ThreadedComment, dispatch_uid='project.save_project_comment_signal')
# def save_project_comment_signal(sender, **kwargs):
#     """ on save of a comment create a notification for the recipient of the comment
#     and log the activity in the event stream """

#     is_new = kwargs.get('created', False)
#     comment = kwargs.get('instance', None)

#     logger.info('Comment is new: %s' % is_new)

#     project = comment.content_object

#     to_user = None

#     if comment.user == project.lawyer.user:
#         to_user = project.customer.user
#     elif comment.user == project.customer.user:
#         to_user = project.lawyer.user
#     else:
#         logger.error('Could not identify the to_user for the comment: %s' % comment.pk)

#     logger.debug('comment is new, so send notification and add to user_stream')
#     # send the comment notifications
#     send_new_comment_notifications(comment=comment, to_user=to_user, project=project)

#     if project and to_user:
#         logger.debug('project and to_user are set')
#         # if this comment is new
#         logger.debug('is_new: %s' % is_new)
#         if is_new:
#             # mark notifications as read
#             """ @BUSINESSRULE mark lawyer project notifications to read: only once they respond """
#             # commented out and made it when the lawyer views the project the same as for founders
#             # if comment.user.profile.is_lawyer:
#             #     mark_project_notifications_as_read(user=comment.user, project=project)

#             """ @BUSINESSRULE if the project request is marked "new" then set it to open only once the lawyer responds """
#             if project.project_status == PROJECT_STATUS.new:
#                 if comment.user.profile.is_lawyer:
#                     project.open(actioning_user=comment.user)


# def send_new_comment_notifications(comment, to_user, project):
#     logger.debug('sending comment notifications to user: %s for project: %s'%(to_user,project.pk,))
#     # send notification
#     notify.send(comment.user, recipient=to_user, verb=u'replied', action_object=project,
#                 description=comment.comment, target=project, project_action='new_project_comment', project_pk=project.pk, lawyer_pk=project.lawyer.user.pk, customer_pk=project.customer.user.pk)
#     # Log activity to stream
#     description = '%s commented on the project' % comment.user


# @receiver(post_save, sender=Notification, dispatch_uid='project.on_comment_notification_created')
# def on_comment_notification_created(sender, **kwargs):
#     """
#     Handle new notifications
#     """
#     notification = kwargs.get('instance')
#     project_action = notification.data.get('project_action', None)

#     if project_action == 'new_project_comment':
#         recipients = [notification.recipient]
#         project = notification.action_object

#         send = SendProjectEmailsService(project=project, sender=notification.actor, recipients=recipients, notification=notification)
#         send.process()
