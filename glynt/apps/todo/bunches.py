# coding: utf-8
""" bunches that allow a simple means of adding a set of todos to a project
per project type,

Bunches DO NOT perform database actions, they ONLY provide the data to be saved
Services is where the magic happens
"""
import os
import yaml

from collections import OrderedDict

from django.template import Context, Template

from glynt.apps.transact import TRANSACTION_TEMPLATE_PATH

from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')


class BaseToDoBunch(Bunch):
    name = None
    template = None
    _todos = OrderedDict()

    def __init__(self, *args, **kwargs):
        self._todos = OrderedDict()

        if not self.name:
            # Set name if not provided
            self.name = self.__class__.__name__.lower().replace('bunch', '')

        super(BaseToDoBunch, self).__init__(*args, **kwargs)

        self.load_template()

    @property
    def todos(self):
        return self._todos

    def categories(self):
        return self._todos.keys() if hasattr(self._todos, 'keys') else []

    def load_template(self):
        """
        Load the .yml template from the templates directory based on class name
        i.e. IncorporationBunch : would load : transact/templates/transactions/incorporation.yml
        """
        if self.template is None:
            self.template = '%s.yml' % self.__class__.__name__.lower().replace('bunch', '')

        if self.template:
            template_file = os.path.join(TRANSACTION_TEMPLATE_PATH, self.template)

            try:
                """ 
                Load the yaml file and update the current object with its data 
                convert the todo set to be a Bunch so we can access it nicely
                """
                with open(template_file) as f:
                    transaction = yaml.safe_load(f).get('transaction')

                    for c, cat_set in enumerate(transaction.get('todos', [])):
                        transaction['todos'][c] = Bunch.fromDict(cat_set)

                    todos = transaction.pop('todos')

                    for t in todos:
                        for cat, data in t.iteritems():
                            self._todos[cat] = data

                    self.__dict__.update(transaction)

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
