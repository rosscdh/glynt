# coding: utf-8
""" bunches that allow a simple means of adding a set of todos to a project
per project type,

Bunches DO NOT perform database actions, they ONLY provide the data to be saved
Services is where the magic happens
"""
import os
import yaml
from django.template import Context, Template

from glynt.apps.transact import TRANSACTION_TEMPLATE_PATH

from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')


class BaseToDoBunch(Bunch):
    name = None
    template = None

    def __init__(self, *args, **kwargs):
        if not self.name:
            # Set name if not provided
            self.name = self.__class__.__name__.lower().replace('bunch', '')

        super(BaseToDoBunch, self).__init__(*args, **kwargs)
        self.load_template()

    def categories(self):
        return self.todos.keys()

    def checklist(self):
        return self.todos

    def load_template(self):
        if not self.template:
            self.template = '%s.yml' % self.__class__.__name__.lower().replace('bunch', '')

        if self.template:
            template_file = os.path.join(TRANSACTION_TEMPLATE_PATH, self.template)
            try:
                with open(template_file) as f:
                    self.__dict__.update(Bunch.fromDict(yaml.safe_load(f).get('transaction')))
            except Exception as ex:
                logger.error('Could not Open %s, due to: %s' % (template_file, ex))

    def attachement(self, attachement_slug):
        """ accessor to allow loading of a document/attachment from the db """
        pass

    def update_todo_context(self, context, todos):
        """ replace the todo name with variables it may contain """
        for todo in todos:
            t = Template(todo.name)
            todo.name = t.render(Context(context))
            todo.save(update_fields=['name'])

# class BaseToDoBunch(Bunch):
#     """ Sets up the todos per transaction + attachments etc """
#     user = None
#     project = None
#     transaction_slug = None
#     required_todo_items = [] # list of todo tuples (name,description,attachements_list) to create. i.e. [('My ToDo', 'Is kinda cool', [FileObject1, FileObject2])]
#     todos = []

#     def __init__(self, user, project=None, *args, **kwargs):
#         self.user = user
#         self.project = project

#         self.transaction_todos()

#         super(BaseToDoBunch, self).__init__(*args, **kwargs)

#     @property
#     def transaction_todos(self):
#         if not self.todos: # python [] epty list evaluates as False
#             # if we dont already have todos then setup a list
#             for name, description, attachments in self.required_todo_items:
#                 self.todos.push( ToDo( user=self.user, \
#                             project=self.project \
#                             name=self.project \
#                             description=self.project )
#                 )
#         return self.todos



# class SeedFundingBunch(BaseToDoBunch):
#     transaction_slug = 'seed-funding'
#     required_todo_items = [('','', [])]
