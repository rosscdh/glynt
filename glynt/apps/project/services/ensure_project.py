# -*- coding: utf-8 -*-
from django import dispatch
from glynt.apps.project.models import Project


import logging
logger = logging.getLogger('lawpal.services')


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

        self.lawyers = kwargs.get('lawyers', [])

        self.company_is_new(company=self.company)

    def company_is_new(self, company):
        """
        Create a new company if it does not exist
        """
        if self.company.pk is None:
            # is a new company
            if self.company.name in [None, '']:
                # give it a name because we dont require the company name anymore
                self.company.name = 'Unnamed company for: %s' % self.customer.user.get_full_name()
            self.company.save()

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

        if self.customer and self.company:
            try:
                self.project = Project.objects.get(customer=self.customer, company=self.company)
                self.is_new = False
                logger.debug('Project exists')

            except:
                self.project = Project.objects.create(customer=self.customer, company=self.company)
                self.project.data['company_name'] = self.company.name
                self.project.save()
                self.is_new = True
                logger.debug('Project created')

            self.process_transactions()
            self.process_lawyers()

        else:
            logger.critical('Proken ensure_project process customer "%s" or company "%s" not present' % (self.customer, self.company,))
