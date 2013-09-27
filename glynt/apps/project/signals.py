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
from glynt.apps.project.services.engage_lawyer_comments import EngageLawyerCommentsMoveService

from glynt.apps.services.pusher import PusherPublisherService

from . import (PROJECT_CREATED, PROJECT_PROFILE_IS_COMPLETE)

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
    if not is_new:

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

@receiver(PROJECT_PROFILE_IS_COMPLETE, dispatch_uid='project.on_project_profile_is_complete')
def on_project_profile_is_complete(sender, **kwargs):
    """
    Handle Project Profile being set as complete
    """
    project = kwargs.get('instance')
    if project:
        # set the project profile_is_complete to True
        project.data['profile_is_complete'] = True
        project.save(update_fields=['data'])


def mark_project_notifications_as_read(user, project):
    """ used to mark the passed in users notifications for a specific project as read (can be either a lawyer or a customer) """
    logger.debug('marking unred notifications as read for user: %s and project: %s' % (user, project.pk))
    Notification.objects.filter(
        recipient=user,
        target_object_id=project.pk,
        unread=True,
        target_content_type=PROJECT_CONTENT_TYPE
    ).mark_all_as_read()


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
                recipients = (instance.lawyer.user,)
                from_name = instance.project.customer.user.get_full_name()
                from_email = instance.project.customer.user.email

                url = instance.project.get_absolute_url()

                logger.info('Sending ProjectLawyer.assigned url:{url}'.format(url=url))
                email = NewActionEmailService(
                    from_name=from_name,
                    from_email=from_email,
                    recipients=recipients,
                    event='project.lawyer_assigned'
                )
                email.send(url=url)

                # copy the comments from the ProjectLawyer object to The Project object to
                # continue the flow
                comments_service = EngageLawyerCommentsMoveService(project_lawyer_join=instance)
                comments_service.process()

                # set all other projectLawyer objects for this project to .rejected
                logger.info('Updating other lawyers assigned as potential ProjectLawyer.assigned email')
                ProjectLawyer.objects.exclude(
                    pk=instance.pk
                ).filter(
                    project=instance.project,
                    status=instance.LAWYER_STATUS.potential
                ).update(
                    status=instance.LAWYER_STATUS.rejected
                )
