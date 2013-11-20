# -*- coding: utf-8 -*-
import json

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
        self.intake_data = json.loads(kwargs.get('intake_data', []))

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
        # set to None
        self.project = None

        if self.customer and self.company:

            try:
                for project in Project.objects.filter(customer=self.customer, company=self.company):

                    # if we find the same set of transactions for this project
                    # then it already exists so use it
                    if project.transactions.all() == self.transactions:
                        # the transactions dont match so raise an error and recreate it
                        self.project = project
                        self.is_new = False
                        break
                    logger.debug('Project exists')

                # project has not been set therefor this is a new project
                if self.project is None:
                    raise Project.DoesNotExist

            except Project.DoesNotExist:
                # this project is new
                self.project = Project.objects.create(customer=self.customer, company=self.company)
                self.project.data['company_name'] = self.company.name
                self.project.data['intake_data'] = self.intake_data
                self.project.save()
                self.is_new = True
                logger.debug('Project created')

            self.process_transactions()
            self.process_lawyers()

        else:
            logger.critical('Proken ensure_project process customer "%s" or company "%s" not present' % (self.customer, self.company,))
