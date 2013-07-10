# coding: utf-8
""" Bunches that prepare and save the pre-validation questions
as well as the transactional info

Bunches DO NOT perform database actions, they ONLY provide the data to be saved
Services is where the magic happens

todos are defined as a tuple of tuples that define the general structure

('todo slug', 'todo name', (
    (Todo, (Validation ruleset)),
    (Todo, (Validation ruleset)),
))

"""
import os
import yaml
from django.template import Context, Template

from . import TRANSACTION_TEMPLATE_PATH

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


class IncorporationBunch(BaseToDoBunch):
    """ class defined the names of fields to extract from a transaction data field """

