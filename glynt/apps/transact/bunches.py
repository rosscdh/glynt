# coding: utf-8
""" Bunches that prepare and save the pre-validation questions
as well as the transactional info

Bunches DO NOT perform database actions, they ONLY provide the data to be saved
Services is where the magic happens
"""
from bunch import Bunch

from glynt.apps.transact.models import Transaction

import logging
logger = logging.getLogger('lawpal.services')


class SeedFundingBunch(Bunch):
    """ class defined the names of fields to extract from a transaction data field """
    transaction_slug = 'seed-funding'