# -*- coding: utf-8 -*-
from bunch import Bunch

import json
import logging
logger = logging.getLogger('lawpal.services')


TRANSACTION_PACKAGES = (('seed_financing_amount','seed','Seed Financing'), 
                        ('incorporation', 'inc', 'Incorporation'), 
                        ('optional', 1, 'optional_funding'), 
                        ('optional', 2, 'optional_funding'), 
                        ('optional', 3, 'optional_funding'),)


class FeePackage(Bunch):
    @property
    def is_valid(self):
        return False if self.title.strip() in [None, ''] else True


class TransactionPackageBunch(object):
    """ Convert the badly implemented transaction packages
    value capture into a neatly portable and predictable object """
    data = None
    key = None
    short = None
    title = None

    packages = {}

    def __init__(self, data):
        self.data = data
        self.packages = self.handle()

    def toJson(self):
        return json.dumps(self.packages)

    def items(self):
        """ Provide a list of valid (valid means they have a title that is not None or empty string) items """
        return [p for key,p in self.packages.iteritems() if p.is_valid]

    @property
    def _fee_present_key(self):
        """ this is necessary due to badly named data keys
        @TODO normalise this at the very least """
        if self.short in ['seed', 'inc']:
            return self.short
        else:
            return self.key

    @property
    def _key(self):
        """ in the case of optional key, the key is not right
        optional_funding1, optional_funding2, optional_funding3
        should be:
        optional1_funding, optional2_funding """
        if self.key == 'optional':
            return '%s%s' % (self.key, self.short if self.short > 1 else '')
        else:
            # if self.short == 'seed': # in the case of seed the key changes
            #return self.short
            return self.key

    @property
    def _title(self):
        """ in the case of optional title where we allow them to insert any value
        the title needs to be set to that value otherwise use the set name """
        if self.key == 'optional':
            data_dict_key = '%s%s' % (self.title, self.short if self.short > 1 else '') # optional title keys look like optional_funding123
            title = self.data.get(data_dict_key, None)
        else:
            title = self.title

        return title

    @property
    def _min_key(self):
        """"""
        if self.key == 'optional':
            return 'optional_min%s' % (self.short if self.short > 1 else '',)
        else:
            return '%s_min' % self.key

    @property
    def _max_key(self):
        """"""
        if self.key == 'optional':
            return 'optional_max%s' % (self.short if self.short > 1 else '',)
        else:
            return '%s_max' % self.key

    def _availablekey_key(self, key):
        """"""
        if self.key == 'optional':
            return '%s%s' % (key, self.short if self.short > 1 else '')
        else:
            return key

    def handle(self):
        """ package the set of items """
        package_items = {}

        for transaction in TRANSACTION_PACKAGES:
            p = {} # setup the package dict

            self.key, self.short, self.title = transaction # assign transaction tuple to class attribs

            p.update({
                'title': self._title,
                'min': self.data.get(self._min_key, 0) if type(self.data.get(self._min_key, 0)) == int else 0,
                'max': self.data.get(self._max_key, 0) if type(self.data.get(self._max_key, 0)) == int else 0,
                'fee_cap_available': True if self.data.get(self._availablekey_key('%s_fee_cap_available' % self._fee_present_key), None) == True else False,
                'deferred_fees_available': True if self.data.get(self._availablekey_key('%s_deferred_fees_available' % self._fee_present_key), None) == True else False,
                'fixed_fees_available': True if self.data.get(self._availablekey_key('%s_fixed_fees_available' % self._fee_present_key), None) == True else False,
            })
            package_items[self._key] = FeePackage(**p)

        return package_items