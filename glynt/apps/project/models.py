# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from uuidfield import UUIDField

from jsonfield import JSONField

from glynt.apps.project.services.actions import OpenProjectService, CloseProjectService, ReOpenProjectService

from glynt.apps.transact.models import Transaction
from glynt.apps.company.models import Company
from glynt.apps.customer.models import Customer
from glynt.apps.lawyer.models import Lawyer

from glynt.apps.project import PROJECT_STATUS

from managers import DefaultProjectManager


class Project(models.Model):
    """ Base Project object
    Stores initial project details
    NB, slug is generated on save if it is not set
    """
    uuid = UUIDField(auto=True, db_index=True)
    customer = models.ForeignKey(Customer)
    company = models.ForeignKey(Company)
    transactions = models.ManyToManyField(Transaction)
    lawyers = models.ManyToManyField(Lawyer, blank=True)
    data = JSONField(default={})
    status = models.IntegerField(choices=PROJECT_STATUS.get_choices(), default=PROJECT_STATUS.new, db_index=True)
    date_created = CreationDateTimeField()
    date_modified = ModificationDateTimeField()

    objects = DefaultProjectManager()

    def __unicode__(self):
        return '%s of %s Project with %s' % (self.customer.user.get_full_name(), self.company, self.get_primary_lawyer(),)

    def get_absolute_url(self):
        return reverse('project:project', kwargs={'slug': self.slug})

    def get_primary_lawyer(self):
        try:
            return self.lawyers.select_related('user').all()[0]
        except IndexError:
            return None

    def open(self, actioning_user):
        """ Open the notification """
        service = OpenProjectService(project=self, actioning_user=actioning_user)
        return service.process()

    def close(self, actioning_user):
        service = CloseProjectService(project=self, actioning_user=actioning_user)
        return service.process()

    def reopen(self, actioning_user):
        service = ReOpenProjectService(project=self, actioning_user=actioning_user)
        return service.process()

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
    def type(self):
        return self.transaction.title

    @property
    def project_status(self):
        return PROJECT_STATUS.get_desc_by_value(self.status)

    @property
    def project_statement(self):
        return self.data.get('project_statement', None)


# import signals so they load on django load
from glynt.apps.project.signals import save_project_comment_signal
