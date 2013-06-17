# -*- coding: utf-8 -*-
from django.db import models

from jsonfield import JSONField


class Transaction(models.Model):
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