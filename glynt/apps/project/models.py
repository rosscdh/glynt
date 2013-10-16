# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from uuidfield import UUIDField
from jsonfield import JSONField

from . import PROJECT_STATUS, PROJECT_LAWYER_STATUS
from .managers import DefaultProjectManager, ProjectLawyerManager
from .mixins import ProjectCategoriesMixin
from .utils import _PROJECT_CONTENT_TYPE

from rulez import registry

import itertools


class Project(ProjectCategoriesMixin, models.Model):
    """ Base Project object
    Stores initial project details
    """
    uuid = UUIDField(auto=True, db_index=True)
    customer = models.ForeignKey('customer.Customer')
    company = models.ForeignKey('company.Company')
    transactions = models.ManyToManyField('transact.Transaction')
    lawyers = models.ManyToManyField('lawyer.Lawyer', blank=True, through='project.ProjectLawyer')
    participants = models.ManyToManyField('auth.User', blank=True)
    data = JSONField(default={})
    status = models.IntegerField(choices=PROJECT_STATUS.get_choices(), default=PROJECT_STATUS.new, db_index=True)
    date_created = CreationDateTimeField()
    date_modified = ModificationDateTimeField()

    objects = DefaultProjectManager()

    def __unicode__(self):
        return u'Project for {company_name}'.format(company_name=self.data.get('company_name', ''))

    def can_read(self, user):
        return True if user.pk in [u.pk for u in self.notification_recipients()] else False

    def can_edit(self, user):
        editors = [self.customer.user] + list([l.user for l in self.lawyers.all()])
        return True if user.pk in [u.pk for u in editors] else False

    def can_delete(self, user):
        editors = [self.customer.user] + list([l.user for l in self.lawyers.all()])
        return True if user.pk in [u.pk for u in editors] else False

    def get_absolute_url(self):
        return reverse('dashboard:project', kwargs={'uuid': str(self.uuid)})

    def get_checklist_absolute_url(self):
        return reverse('dashboard:checklist', kwargs={'uuid': str(self.uuid)})

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
    def content_type_id(self):
        return _PROJECT_CONTENT_TYPE().pk

    @property
    def pusher_id(self):
        return str(self.uuid)

    @property
    def primary_lawyer(self):
        return self.get_primary_lawyer()

    def get_primary_lawyer(self):
        try:
            primary_lawyer_join = ProjectLawyer.objects.assigned(project=self)[0]
            return primary_lawyer_join.lawyer
        except:
            return None

    def notification_recipients(self):
        """
        provide access to the customer, the lawyer
        ### not yet ### as well as any user associated with the customers company ## end not yet ##
        """
        return self.participants.all()

    @property
    def has_lawyer(self):
        return ProjectLawyer.objects.assigned(project=self).count() > 0

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
    def transaction_slugs(self):
        return [t.slug for t in self.transactions.all()]

    @property
    def transaction_types(self):
        return [t.title for t in self.transactions.all()]

    @property
    def tx_range(self):
        return ','.join(self.transaction_slugs)

    @property
    def display_status(self):
        return PROJECT_STATUS.get_desc_by_value(self.status)

    @property
    def project_statement(self):
        return self.data.get('project_statement', None)

registry.register("can_read", Project)
registry.register("can_edit", Project)
registry.register("can_delete", Project)


class ProjectLawyer(models.Model):
    """
    The customised variation of a generic m2m model
    msut be named ProjectLawyer(s) <-- this is not noraml for django
    """
    LAWYER_STATUS = PROJECT_LAWYER_STATUS

    project = models.ForeignKey('project.Project')
    lawyer = models.ForeignKey('lawyer.Lawyer')
    status = models.IntegerField(choices=LAWYER_STATUS.get_choices(), default=LAWYER_STATUS.potential, db_index=True)

    objects = ProjectLawyerManager()

    class Meta:
        db_table = 'project_project_lawyer'

    @property
    def display_status(self):
        return self.LAWYER_STATUS.get_desc_by_value(self.status)

    def notification_recipients(self):
        """
        """
        return [self.project.customer.user, self.lawyer.user]

    def get_absolute_url(self):
        return reverse('project:project_contact', kwargs={'slug': self.project.uuid, 'lawyer': self.lawyer.user.username})


from .signals import (on_project_created, on_save_ensure_user_in_participants, 
                      on_lawyer_assigned,
                      lawyer_on_save_ensure_participants,
                      lawyer_on_delete_ensure_participants,)