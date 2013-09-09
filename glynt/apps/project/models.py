# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from uuidfield import UUIDField

from jsonfield import JSONField

#from glynt.apps.project.services.actions import OpenProjectService, CloseProjectService, ReOpenProjectService

from glynt.apps.transact.models import Transaction
from glynt.apps.company.models import Company
from glynt.apps.lawyer.models import Lawyer

from . import PROJECT_STATUS, PROJECT_LAWYER_STATUS
from .managers import DefaultProjectManager, ProjectLawyerManager

from rulez import registry

import itertools


class Project(models.Model):
    """ Base Project object
    Stores initial project details
    """
    _primary_lawyer = False

    uuid = UUIDField(auto=True, db_index=True)
    customer = models.ForeignKey('customer.Customer')
    company = models.ForeignKey(Company)
    transactions = models.ManyToManyField(Transaction)
    lawyers = models.ManyToManyField(Lawyer, blank=True, through='project.ProjectLawyer')
    data = JSONField(default={})
    status = models.IntegerField(choices=PROJECT_STATUS.get_choices(), default=PROJECT_STATUS.new, db_index=True)
    date_created = CreationDateTimeField()
    date_modified = ModificationDateTimeField()

    objects = DefaultProjectManager()

    def __unicode__(self):
        return 'Project for {company}'.format(company=self.company.name)

    def can_read(self, user):
        return True if user.pk in [u.pk for u in self.notification_recipients()] else False

    def can_edit(self, user):
        return True if user.pk in [u.pk for u in self.notification_recipients()] else False

    def get_absolute_url(self):
        return reverse('dashboard:project', kwargs={'uuid': self.uuid})

    def get_checklist_absolute_url(self):
        return reverse('dashboard:checklist', kwargs={'uuid': self.uuid})

    def checklist(self):
        """
        Load all of the projects transaction types
        and extract their bunch classes (based on yml files)
        """
        checklist_items = []

        for t in self.transactions.all():
            checklist_items += t.checklist()

        return checklist_items

    @property
    def primary_lawyer(self):
        return self.get_primary_lawyer()

    def get_primary_lawyer(self):
        if self._primary_lawyer is False:
            try:
                _primary_lawyer = self.lawyers.select_related('user').all()[0]
            except:
                _primary_lawyer = None
        return _primary_lawyer

    def notification_recipients(self):
        return itertools.chain(self.company.customers.all(), [l.user for l in self.lawyers.all()])

    @property
    def has_lawyer(self):
        return ProjectLawyer.objects.assigned(project=self).count() > 0

    # def open(self, actioning_user):
    #     """ Open the notification """
    #     service = OpenProjectService(project=self, actioning_user=actioning_user)
    #     return service.process()

    # def close(self, actioning_user):
    #     service = CloseProjectService(project=self, actioning_user=actioning_user)
    #     return service.process()

    # def reopen(self, actioning_user):
    #     service = ReOpenProjectService(project=self, actioning_user=actioning_user)
    #     return service.process()

    @property
    def is_open(self):
        return PROJECT_STATUS.open == self.status

    @property
    def is_closed(self):
        return PROJECT_STATUS.closed == self.status

    @property
    def is_new(self):
        return PROJECT_STATUS.new == self.status

    @property
    def transaction_types(self):
        return [t.title for t in self.transactions.all()]

    @property
    def tx_range(self):
        return ','.join([t.slug for t in self.transactions.all()])

    @property
    def display_status(self):
        return PROJECT_STATUS.get_desc_by_value(self.status)

    @property
    def project_statement(self):
        return self.data.get('project_statement', None)

registry.register("can_read", Project)
registry.register("can_edit", Project)


class ProjectLawyer(models.Model):
    """
    The customised variation of a generic m2m model
    msut be named ProjectLawyer(s) <-- this is not noraml for django
    """
    LAWYER_STATUS = PROJECT_LAWYER_STATUS

    project = models.ForeignKey(Project)
    lawyer = models.ForeignKey(Lawyer)
    status = models.IntegerField(choices=LAWYER_STATUS.get_choices(), default=LAWYER_STATUS.potential, db_index=True)

    objects = ProjectLawyerManager()

    class Meta:
        db_table = 'project_project_lawyer'

    @property
    def display_status(self):
        return self.LAWYER_STATUS.get_desc_by_value(self.status)


# import signals so they load on django load
from glynt.apps.project.signals import on_project_created, on_lawyer_assigned
