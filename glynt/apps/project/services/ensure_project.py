# -*- coding: utf-8 -*-
from django import dispatch
from glynt.apps.project.models import Project


import logging
logger = logging.getLogger('lawpal.services')


PROJECT_CREATED = dispatch.Signal(providing_args=["created", "instance"])
PROJECT_PROFILE_IS_COMPLETE = dispatch.Signal(providing_args=["instance"])


class EnsureProjectService(object):
    """
    Ensure that a project exists given:
    a customer, company and at least 1 transaction_type
    """
    lawyers = []

    def __init__(self, customer, company, transactions, **kwargs):
        logger.info('Started Ensure Project')
        self.customer = customer
        self.company = company
        self.transactions = transactions
        self.data = kwargs
        self.pk = kwargs.get('pk', False)
        self.lawyers = kwargs.get('lawyers', [])

    def process_transactions(self):
        logger.info('Processing Project Transactions')
        if len(self.transactions) > 0:
            for transaction in self.transactions:
                self.project.transactions.add(transaction)

    def process_lawyers(self):
        logger.info('Processing Project Lawyers')
        if len(self.lawyers) > 0:
            for lawyer in self.lawyers:
                self.project.lawyers.add(lawyer)

    def process(self):
        logger.debug('Processing Project')

        if self.pk is False:

            try:
                self.project = Project.objects.get(customer=self.customer, company=self.company)
                self.is_new = False
                logger.debug('Project exists')

            except Project.DoesNotExist:
                self.project = Project.objects.create(customer=self.customer, company=self.company)
                self.is_new = True
                logger.debug('Project created')

            #self.project, self.is_new = Project.objects.get_or_create(**{'customer': self.customer, 'company': self.company}) # Causes big problems

        else:
            self.project = Project.objects.filter(pk=self.pk)
            self.is_new = False

        self.project.customer = self.customer
        self.project.company = self.company

        self.process_transactions()
        self.process_lawyers()
        self.project.save()
