# coding: utf-8
from django.template.defaultfilters import slugify
from glynt.apps.company.models import Company

import logging
logger = logging.getLogger('lawpal.services')


class EnsureCompanyService(object):
    """ Set up a startup """
    customer = None
    startup = None

    def __init__(self, name, customer=None, **kwargs):
        self.company_name = name
        self.customer = customer
        self.slug = kwargs.pop('slug', None)
        self.summary = kwargs.pop('summary', None)
        self.website = kwargs.pop('website', None)
        self.twitter = kwargs.pop('twitter', None)
        self.photo = kwargs.pop('photo', None)
        self.data = kwargs

    def add_customer(self, customer=None):
        if self.customer or customer:
            customer = customer if customer else self.customer
            if not self.company:
                raise Exception('Company has not yet been defined for service, need to call .process()')

            self.company.customers.remove(customer.user) # ensure he is not already assocaited with the startup
            self.company.customers.add(customer.user)

    def process(self):
        self.company, is_new = Company.objects.get_or_create(name=self.company_name)
        logger.info("Processing startup %s (is_new: %s)" % (self.company, is_new,))

        self.add_customer(self.customer)

        if self.slug or is_new:
            self.company.slug = self.slug if self.slug else slugify(self.company_name)

        if self.summary:
            self.company.summary = self.summary

        if self.website:
            self.company.website = self.website

        if self.twitter:
            self.company.twitter = self.twitter

        if self.data:
            self.company.data = self.data

        logger.info("Saving startup %s", self.company_name)
        self.company.save()

        return self.company
