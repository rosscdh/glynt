# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from glynt.apps.todo.models import Attachment

from bunch import Bunch
from actstream import action

import json
import logging
logger = logging.getLogger('lawpal.services')


class CrocdocWebhookService(object):
    payload = None

    def __init__(self, payload=payload, *args, **kwargs):
        self.user = kwargs.get('user')
        self.payload = json.loads(payload)
        self.items = [Bunch(**i) for i in self.payload]

    def process(self):
        page = None
        for c, i in enumerate(self.items):
            #print '{num}: Item: {i}'.format(num=c, i=i)
            event = i.get('event')
            event_type = i.get('type')
            if i.get('page') is not None:
                page = i.get('page')

            print "{event} is of type {event_type} on page: {page}".format(event_type=event_type, event=event, page=page)

            if event == 'comment.create':
                i = CrocdocCommentCreateEvent(page=page, **i)

            elif event == 'annotation.create':

                if event_type == 'textbox':
                    i = CrocdocAnnotationTextboxEvent(**i)

                elif event_type == 'highlight':
                    i = CrocdocAnnotationHighlightEvent(**i)

                elif event_type == 'strikeout':
                    i = CrocdocAnnotationStrikeoutEvent(**i)

                elif event_type == 'drawing':
                    i = CrocdocAnnotationDrawingEvent(**i)

            elif event == 'comment.delete':
                i = CrocdocCommentDeleteEvent(**i)

            i.process() if hasattr(i, 'process') else None


class CrocdocBaseEvent(Bunch):
    _user = None
    _attachment = None
    content = None
    event = None
    type = None
    owner = None
    page = None
    doc = None
    uuid = None

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        super(CrocdocBaseEvent, self).__init__(*args, **kwargs)

    @property
    def user(self):
        """ Crocdoc provides userid as string(pk,user_name)"""
        if self._user is None:
            pk, full_name = self.owner.split(',')
            pk = int(pk)
            self._user = User.objects.get(pk=pk)
        return self._user

    @property
    def attachment(self):
        if self._attachment is None:
            self._attachment = Attachment.objects.get(uuid=self.doc)
        return self._attachment


class CrocdocCommentCreateEvent(CrocdocBaseEvent):
    def process(self):
        action.send(self.user, 
                    verb='Commented on an Attachment',
                    action_object=self.attachment, 
                    target=self.attachment.todo,
                    attachment_name=self.attachment.filename,
                    **self.toDict())


class CrocdocCommentDeleteEvent(CrocdocBaseEvent):
    def process(self):
        action.send(self.user, 
                    verb='Deleted a Commented on an Attachment',
                    action_object=self.attachment, 
                    target=self.attachment.todo,
                    attachment_name=self.attachment.filename,
                    **self.toDict())


class CrocdocAnnotationHighlightEvent(CrocdocBaseEvent):
    def process(self):
        action.send(self.user, 
                    verb='Hilighted some text on an Attachment',
                    action_object=self.attachment,
                    target=self.attachment.todo,
                    attachment_name=self.attachment.filename,
                    **self.toDict())


class CrocdocAnnotationStrikeoutEvent(CrocdocBaseEvent):
    def process(self):
        action.send(self.user, 
                    verb='Struck out some text on an Attachment',
                    action_object=self.attachment,
                    target=self.attachment.todo,
                    attachment_name=self.attachment.filename,
                    **self.toDict())



class CrocdocAnnotationTextboxEvent(CrocdocBaseEvent):
    def process(self):
        action.send(self.user, 
                    verb='Added a text element on an Attachment',
                    action_object=self.attachment,
                    target=self.attachment.todo,
                    attachment_name=self.attachment.filename,
                    **self.toDict())


class CrocdocAnnotationDrawingEvent(CrocdocBaseEvent):
    def process(self):
        action.send(self.user, 
                    verb='Added a drawing element on an Attachment',
                    action_object=self.attachment,
                    target=self.attachment.todo,
                    attachment_name=self.attachment.filename,
                    **self.toDict())
