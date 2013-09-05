# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.dispatch import receiver
from django.db.models.signals import pre_save

from notifications import notify

from notifications.models import Notification

from glynt.apps.services.email import NewActionEmailService

from glynt.apps.project.utils import PROJECT_CONTENT_TYPE

from glynt.apps.project.services.email import SendNewProjectEmailsService
from glynt.apps.project.services.project_checklist import ProjectCheckListService
from glynt.apps.project.services.ensure_project import PROJECT_CREATED
from glynt.apps.project.services.engage_lawyer_comments import EngageLawyerCommentsMoveService

from .models import ProjectLawyer


import logging
logger = logging.getLogger('django.request')


@receiver(PROJECT_CREATED, dispatch_uid='project.on_project_created')
def on_project_created(sender, **kwargs):
    """
    Handle new Project
    """
    is_new = kwargs.get('created')
    project = kwargs.get('instance')

    # ensure that we have a project object and that is has NO pk 
    # as we dont want this event to happen on change of a project
    if project and project.pk is None:
        # set the project profile_is_complete to True
        project.data['profile_is_complete'] = True
        project.save(update_fields=['data'])

        user = project.customer.user
        comment = u'{user} created this Project'.format(user=user.get_full_name())
        logger.debug(comment)

        # send notification
        notify.send(user, recipient=user, verb=u'created', action_object=project,
                    description=comment, target=project, project_action='created_project', project_pk=project.pk, creating_user_pk=user.pk)

        send = SendNewProjectEmailsService(project=project, sender=user)
        send.process()

    # perform the bulk create event
    # to bring project up to date with any modifications made
    checklist_service = ProjectCheckListService(project=project)
    checklist_service.bulk_create()


def mark_project_notifications_as_read(user, project):
    """ used to mark the passed in users notifications for a specific project as read (can be either a lawyer or a customer) """
    logger.debug('marking unred notifications as read for user: %s and project: %s'%(user, project.pk))
    Notification.objects.filter(recipient=user, target_object_id=project.pk, unread=True, target_content_type=PROJECT_CONTENT_TYPE).mark_all_as_read()


@receiver(pre_save, sender=ProjectLawyer, dispatch_uid='project.lawyer_assigned')
def on_lawyer_assigned(sender, **kwargs):
    instance = kwargs.get('instance')

    if instance.pk is not None:
        # we have an existing item
        prev_instance = ProjectLawyer.objects.get(pk=instance.pk)

        if prev_instance.status != instance.status:

            if instance.status == instance.LAWYER_STATUS.assigned:
                logger.info('Sending ProjectLawyer.assigned email')
                # send email of congratulations to lawyer in question
                subject = 'Congratulations, You have been selected for a LawPal.com project'

                message = 'You have been selected to work on a project for {customer} of {company}. \
                The project consists of the following transaction types: {transactions}\
                Please review the project at the url below'.format(customer=instance.project.customer, \
                                                                   company=instance.project.company, \
                                                                   transactions=','.join(instance.project.transaction_types))
                recipients = (instance.lawyer.user,)
                from_name = instance.project.customer.user.get_full_name()
                from_email = instance.project.customer.user.email

                url = instance.project.get_absolute_url()

                logger.info('Sending ProjectLawyer.assigned url:{url}'.format(url=url))
                email = NewActionEmailService(subject=subject, message=message, from_name=from_name, from_email=from_email, recipients=recipients)
                email.send(url=url)

                # copy the comments from the ProjectLawyer object to The Project object to
                # continue the flow
                comments_service = EngageLawyerCommentsMoveService(project_lawyer_join=instance)
                comments_service.process()

                # set all other projectLawyer objects for this project to .rejected
                logger.info('Updating other lawyers assigned as potential ProjectLawyer.assigned email')
                ProjectLawyer.objects.exclude(pk=instance.pk) \
                                    .filter(project=instance.project, \
                                            status=instance.LAWYER_STATUS.potential) \
                                    .update(status=instance.LAWYER_STATUS.rejected)

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
#             if project.display_status == PROJECT_STATUS.new:
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
