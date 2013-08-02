# -*- coding: utf-8 -*-
#from django.contrib.contenttypes.models import ContentType

from actstream.managers import ActionManager, stream

class LawpalStreamActionManager(ActionManager):

    @stream
    def todo_item_stream(self, obj, verb='posted', time=None):
        if time is None:
            time = datetime.now()
        return obj.actor_actions.filter(verb = verb, timestamp__lte = time)

    @stream
    def project_stream(self, obj, verb='posted', time=None):
        if time is None:
            time = datetime.now()
        return obj.actor_actions.filter(verb = verb, timestamp__lte = time)