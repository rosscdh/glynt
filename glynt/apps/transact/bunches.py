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
from glynt.apps.todo.bunches import BaseToDoBunch

import logging
logger = logging.getLogger('lawpal.services')


class IncorporationBunch(BaseToDoBunch):
    """ class defined the names of fields to extract from a transaction data field """


class SeedFundingEquityRoundBunch(BaseToDoBunch):
    """ class defined the names of fields to extract from a transaction data field """


class SeedFundingConvertibleNoteBunch(BaseToDoBunch):
    """ class defined the names of fields to extract from a transaction data field """
