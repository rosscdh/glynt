# coding: utf-8
""" bunches that allow a simple means of adding a set of todos to an engagement
per engagement type,

Bunches DO NOT perform database actions, they ONLY provide the data to be saved
Services is where the magic happens
"""
from bunch import Bunch

from glynt.apps.todo.models import ToDo

import logging
logger = logging.getLogger('lawpal.services')


class BaseToDoBunch(Bunch):
    """ Sets up the todos per transaction + attachments etc """
    user = None
    engagement = None
    transaction_slug = None
    required_todo_items = [] # list of todo tuples (name,description,attachements_list) to create. i.e. [('My ToDo', 'Is kinda cool', [FileObject1, FileObject2])]
    todos = []

    def __init__(self, user, engagement=None, *args, **kwargs):
        self.user = user
        self.engagement = engagement

        self.transaction_todos()

        super(BaseToDoBunch, self).__init__(*args, **kwargs)

    @property
    def transaction_todos(self):
        if not self.todos: # python [] epty list evaluates as False
            # if we dont already have todos then setup a list
            for name, description, attachments in self.required_todo_items:
                self.todos.push( ToDo( user=self.user, \
                            engagement=self.engagement \
                            name=self.engagement \
                            description=self.engagement )
                )
        return self.todos



class SeedFundingBunch(BaseToDoBunch):
    transaction_slug = 'seed-funding'
    required_todo_items = [('','', [])]