# -*- coding: utf-8 -*-
""" Set of signals to handle when comments are posted and assigning notifications to the user """
from django.db.models.signals import post_save
from django.dispatch import receiver

from threadedcomments.models import ThreadedComment # if we stop using threadedcomments this model will change

from notifications import notify
import user_streams

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=ThreadedComment, dispatch_uid='engage.comments.save_engage_comment_signal')
def save_engage_comment_signal(sender, **kwargs):
    """ on save of a comment create a notification for the recipient of the comment
    and log the activity in the event stream """

    is_new = kwargs.get('created', False)
    comment = kwargs.get('instance', None)

    if comment:
        logger.debug('we have a comment')
        engagement = comment.content_object
        logger.debug('engagement object: %s'%engagement)
        to_user = None

        if comment.user == engagement.lawyer.user:
            to_user = engagement.founder.user
        elif comment.user == engagement.founder.user:
            to_user = engagement.lawyer.user
        else:
            logger.error('Could not identify the to_user for the comment: %s' % comment.pk)

        if engagement and to_user:
            logger.debug('engagement and to_user are set')
            if is_new:
                logger.debug('comment is new, so send notification and add to user_stream')
                # send notification
                notify.send(comment.user, recipient=to_user, verb=u'replied', action_object=comment,
                            description=comment.comment, target=engagement, engagement_pk=engagement.pk, lawyer_pk=engagement.lawyer.user.pk, founder_pk=engagement.founder.user.pk)
                # Log activity to stream
                description = '%s commented on the engagement' % comment.user
                user_streams.add_stream_item(to_user, description, engagement)
                user_streams.add_stream_item(comment.user, description, engagement)