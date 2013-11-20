# -*- coding: utf-8 -*-
"""
Action Created Events - which is involked everytime action.send is called
@PRIMARY HANDLER
"""
from django.dispatch import receiver
from django.db.models.signals import post_save

from bunch import Bunch

from actstream.models import Action

from glynt.apps.services.email import NewActionEmailService
from glynt.apps.services.pusher import PusherPublisherService

import logging
logger = logging.getLogger('django.request')


@receiver(post_save, sender=Action, dispatch_uid='action.created')
def on_action_created(sender, **kwargs):
    """
    Handle Creation of attachments
    """
    if sender.__name__ != 'LogEntry':
        is_new = kwargs.get('created', False)
        action = kwargs.get('instance')
        target = action.target

        if action and is_new:

            event = action.data.get('event', 'action.created')

            user_name = action.actor.get_full_name()
            user_email = action.actor.email

            info_object = Bunch(name=user_name,
                                verb=action.verb,
                                target_name=unicode(action),
                                timestamp='',
                                **action.data)

            # if the target has a project attached to it
            if hasattr(target, 'pusher_id'):
                if hasattr(target, 'project'):
                    # send the same event to the project channel
                    # so that the other project channel subscribers
                    # can hear it
                    channels = [target.project.pusher_id, target.pusher_id]
                    pusher_service = PusherPublisherService(channel=channels, event=event)
                else:
                    pusher_service = PusherPublisherService(channel=target.pusher_id, event=event)

                pusher_service.process(label=action.verb, comment=action.verb, **info_object)

            recipients = None
            url = None

            target_type = target.__class__.__name__

            if target_type == 'Project':
                logger.debug('action.target is a Project object')
                project = target
                recipients = project.notification_recipients()
                url = action.data.get('url', project.get_absolute_url())

            elif target_type == 'ProjectLawyer':
                logger.debug('action.target is a ProjectLawyer object')
                project = target.project
                recipients = target.notification_recipients()
                url = action.data.get('url', project.get_absolute_url()) # @TODO need to change this to be the actual engagement element link and write a js trigger to show the modal

            elif target_type == 'ToDo':
                logger.debug('action.target is a ToDo object')
                project = action.target.project
                recipients = project.notification_recipients()
                url = action.data.get('url', target.get_absolute_url())  # get the todos absolute url

            if recipients:
                logger.debug('recipients: {recipients}'.format(recipients=recipients))

                email = NewActionEmailService(
                    verb=event,
                    from_name=user_name,
                    from_email=user_email,
                    recipients=recipients,
                    actor=action.actor,
                    target=target,
                    project=project,
                    **action.data  # append kwargs sent in via: https://django-activity-stream.readthedocs.org/en/latest/data.html
                )
                email.send(url=url, message=action.verb)
