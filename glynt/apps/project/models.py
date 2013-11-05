# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from uuidfield import UUIDField
from jsonfield import JSONField

from glynt.apps.project import PROJECT_STATUS, PROJECT_LAWYER_STATUS
from glynt.apps.project.managers import DefaultProjectManager, ProjectLawyerManager
from glynt.apps.project.mixins import ProjectCategoriesMixin, ProjectRulezMixin

from rulez import registry as rulez_registry


class Project(ProjectCategoriesMixin, ProjectRulezMixin, models.Model):
    """ Base Project object
    Stores initial project details
    """
    _PROJECT_STATUS = PROJECT_STATUS

    uuid = UUIDField(auto=True, db_index=True)
    customer = models.ForeignKey('customer.Customer')
    company = models.ForeignKey('company.Company', blank=True, null=True)
    transactions = models.ManyToManyField('transact.Transaction')
    lawyers = models.ManyToManyField('lawyer.Lawyer', blank=True, through='project.ProjectLawyer')
    participants = models.ManyToManyField('auth.User', blank=True)
    data = JSONField(default={})
    status = models.IntegerField(choices=PROJECT_STATUS.get_choices(), default=PROJECT_STATUS.new, db_index=True)
    date_created = CreationDateTimeField()
    date_modified = ModificationDateTimeField()

    objects = DefaultProjectManager()

    def __unicode__(self):
        return self.data.get('project_name', self.project_name())

    @staticmethod
    def content_type():
        """
        Static method used to access the content type of projects
        """
        return ContentType.objects.get_for_model(Project)

    @property
    def content_type_id(self):
        return Project.content_type().pk

    @property
    def pusher_id(self):
        return str(self.uuid)

    def project_name(self):
        return u'Project for {customer} {transactions}'.format(customer=self.customer.user.get_full_name(),
                                                   transactions=', '.join(self.transaction_types))

    @property
    def primary_lawyer(self):
        return self.get_primary_lawyer()

    @property
    def has_lawyer(self):
        from glynt.apps.project.models import ProjectLawyer
        return ProjectLawyer.objects.assigned(project=self).count() > 0

    @property
    def is_open(self):
        return self._PROJECT_STATUS.open == self.status

    @property
    def is_closed(self):
        return self._PROJECT_STATUS.closed == self.status

    @property
    def is_new(self):
        return self._PROJECT_STATUS.new == self.status

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
        return self._PROJECT_STATUS.get_desc_by_value(self.status)

    @property
    def project_statement(self):
        return self.data.get('project_statement', None)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('dashboard:project', kwargs={'uuid': str(self.uuid)})

    def get_checklist_absolute_url(self):
        from django.core.urlresolvers import reverse
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

    def get_primary_lawyer(self):
        from glynt.apps.project.models import ProjectLawyer
        try:
            primary_lawyer_join = ProjectLawyer.objects.assigned(project=self)[0]
            return primary_lawyer_join.lawyer
        except IndexError:
            return None

    def notification_recipients(self):
        """
        provide access to the customer, the lawyer
        ### not yet ### as well as any user associated with the customers company ## end not yet ##
        """
        return self.participants.all()


class ProjectLawyer(models.Model):
    """
    The customised variation of a generic m2m model
    msut be named ProjectLawyer(s) <-- this is not noraml for django
    """
    _LAWYER_STATUS = PROJECT_LAWYER_STATUS

    project = models.ForeignKey('project.Project')
    lawyer = models.ForeignKey('lawyer.Lawyer')
    status = models.IntegerField(choices=_LAWYER_STATUS.get_choices(), default=_LAWYER_STATUS.potential, db_index=True)

    objects = ProjectLawyerManager()

    class Meta:
        db_table = 'project_project_lawyer'

    @property
    def display_status(self):
        return self._LAWYER_STATUS.get_desc_by_value(self.status)

    def notification_recipients(self):
        """
        """
        return [self.project.customer.user, self.lawyer.user]

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('project:project_contact', kwargs={'slug': self.project.uuid, 'lawyer': self.lawyer.user.username})


"""
The signal connections are handled here as the signals are imported a number of
the imports in this file will cause circular imports
"""
from .signals import (on_project_created,
                      on_save_ensure_user_in_participants, 
                      on_lawyer_assigned,
                      on_project_categories_sort_updated,
                      on_project_profile_is_complete,
                      lawyer_on_save_ensure_participants,
                      lawyer_on_delete_ensure_participants,)


rulez_registry.register("can_read", Project)
rulez_registry.register("can_edit", Project)
rulez_registry.register("can_delete", Project)
