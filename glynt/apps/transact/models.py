# -*- coding: utf-8 -*-
from django.db import models

from jsonfield import JSONField

from . import import_module_class

import logging
logger = logging.getLogger('django.request')


class Transaction(models.Model):
    """
    Each Transcation record will load data form the list
    specified in the data field of the transaction record (to allow for multiple sets of .yml files)
    i.e. fixture looks like this

      "data": {
        "checklist_bunches": [
          "IncorporationBunch"
        ]
      },

    refers to a Bunch class (bunches.py) which in turn will load a .yml file
    the bunch class allows us to parse and do clever custom things to the yml 
    file entries
    """
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    data = JSONField(default={})

    def __unicode__(self):
        return u'%s, %s' % (self.title, self.display_price,)

    @property
    def display_price(self):
        return "%01.2f" % self.price

    def checklist(self):
        checklist_items = []

        for b in self.data.get('checklist_bunches', []):
            BunchClass = import_module_class('glynt.apps.transact.bunches.{bunch}'.format(bunch=b))

            if BunchClass is not None:
                bunch = BunchClass()
                checklist_items.append(bunch)
            else:
                logger.critical('Could not import Transaction bunch {bunch}'.format(bunch=b))

        return checklist_items
