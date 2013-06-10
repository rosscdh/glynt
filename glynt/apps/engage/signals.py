# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.db.models.signals import post_save
from django.dispatch import receiver

from threadedcomments.models import ThreadedComment # if we stop using threadedcomments this model will change
from notifications import notify
import user_streams

from notifications.models import Notification
from glynt.apps.engage.utils import ENGAGEMENT_CONTENT_TYPE
from glynt.apps.engage.models import Engagement, ENGAGEMENT_STATUS
from glynt.apps.engage.services.email import SendEngagementEmailsService

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=ThreadedComment, dispatch_uid='engagement.save_engagement_comment_signal')
def save_engagement_comment_signal(sender, **kwargs):
    """ on save of a comment create a notification for the recipient of the comment
    and log the activity in the event stream """

    is_new = kwargs.get('created', False)
    comment = kwargs.get('instance', None)

    logger.info('Comment is new: %s'%is_new)

    engagement = comment.content_object

    to_user = None

    if comment.user == engagement.lawyer.user:
        to_user = engagement.founder.user
    elif comment.user == engagement.founder.user:
        to_user = engagement.lawyer.user
    else:
        logger.error('Could not identify the to_user for the comment: %s' % comment.pk)


    logger.debug('comment is new, so send notification and add to user_stream')
    # send the comment notifications
    send_new_comment_notifications(comment=comment, to_user=to_user, engagement=engagement)

    if engagement and to_user:
        logger.debug('engagement and to_user are set')
        # if this comment is new
        logger.debug('is_new: %s' % is_new)
        if is_new:
            # mark notifications as read
            """ @BUSINESSRULE mark lawyer engagement notifications to read: only once they respond """
            # commented out and made it when the lawyer views the engagement the same as for founders
            # if comment.user.profile.is_lawyer:
            #     mark_engagement_notifications_as_read(user=comment.user, engagement=engagement)

            """ @BUSINESSRULE if the engagement request is marked "new" then set it to open only once the lawyer responds """
            if engagement.engagement_status == ENGAGEMENT_STATUS.new:
                if comment.user.profile.is_lawyer:
                    engagement.open(actioning_user=comment.user)


def send_new_comment_notifications(comment, to_user, engagement):
    logger.debug('sending comment notifications to user: %s for engagement: %s'%(to_user,engagement.pk,))
    # send notification
    notify.send(comment.user, recipient=to_user, verb=u'replied', action_object=engagement,
                description=comment.comment, target=engagement, engagement_action='new_engagement_comment', engagement_pk=engagement.pk, lawyer_pk=engagement.lawyer.user.pk, founder_pk=engagement.founder.user.pk)
    # Log activity to stream
    description = '%s commented on the engagement' % comment.user
    user_streams.add_stream_item(to_user, description, engagement)
    user_streams.add_stream_item(comment.user, description, engagement)


def mark_engagement_notifications_as_read(user, engagement):
    """ used to mark the passed in users notifications for a specific engagement as read (can be either a lwayer or a founder) """
    logger.debug('marking unred notifications as read for user: %s and engagement: %s'%(user, engagement.pk))
    Notification.objects.filter(recipient=user, target_object_id=engagement.pk, unread=True, target_content_type=ENGAGEMENT_CONTENT_TYPE).mark_all_as_read()


@receiver(post_save, sender=Notification, dispatch_uid='engagement.on_engagement_created')
def on_engagement_created(sender, **kwargs):
    """
    Handle new Engagement
    """
    is_new = kwargs.get('created')

    notification = kwargs.get('instance')
    engagement_action = notification.data.get('engagement_action', None)

    if is_new is True and engagement_action is not None:

        if engagement_action == 'engagement_created':
            recipients = [notification.recipient]
            engagement = notification.action_object

            send = SendEngagementEmailsService(engagement=engagement, sender=notification.actor, recipients=recipients, notification=notification, is_new_engagement=True)
            send.process()


@receiver(post_save, sender=Notification, dispatch_uid='engagement.on_comment_notification_created')
def on_comment_notification_created(sender, **kwargs):
    """
    Handle new notifications
    """
    is_new = kwargs.get('created')

    notification = kwargs.get('instance')
    engagement_action = notification.data.get('engagement_action', None)

    if engagement_action == 'new_engagement_comment':
        recipients = [notification.recipient]
        engagement = notification.action_object

        send = SendEngagementEmailsService(engagement=engagement, sender=notification.actor, recipients=recipients, notification=notification)
        send.process()


