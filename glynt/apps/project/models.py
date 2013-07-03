# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from jsonfield import JSONField

from glynt.apps.utils import generate_unique_slug

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
    transaction = models.ForeignKey(Transaction, null=True)
    project_status = models.IntegerField(choices=PROJECT_STATUS.get_choices(), default=PROJECT_STATUS.new, db_index=True)
    slug = models.SlugField(max_length=128, blank=False)
    startup = models.ForeignKey(Company)
    customer = models.ForeignKey(Customer)
    lawyer = models.ForeignKey(Lawyer)
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    objects = DefaultProjectManager()

    def __unicode__(self):
        return '%s of %s Project with %s' % (self.customer.user.get_full_name(), self.startup, self.lawyer.user.get_full_name(),)

    def get_absolute_url(self):
        return reverse('project:project', kwargs={'slug': self.slug})

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
        return PROJECT_STATUS.open == self.project_status

    @property
    def is_closed(self):
        return PROJECT_STATUS.closed == self.project_status

    @property
    def is_new(self):
        return PROJECT_STATUS.new == self.project_status

    @property
    def type(self):
        return self.transaction.title

    @property
    def status(self):
        return PROJECT_STATUS.get_desc_by_value(self.project_status)

    @property
    def project_statement(self):
        return self.data.get('project_statement', None)

    @property
    def project_types(self):
        project_types = [('engage_for_general','General'), ('engage_for_incorporation','Incorporation'), ('engage_for_ip','Intellectual Property'), ('engage_for_employment','Employment Law'), ('engage_for_fundraise','Fundraising'), ('engage_for_cofounders','Co-Customer')]
        return [(self.data.get(r,False),name) for r,name in project_types if self.data.get(r,False)]

    def save(self, *args, **kwargs):
        """ Ensure that we have a slug """
        if self.slug in [None, '']:
            self.slug = generate_unique_slug(instance=self)

        return super(Project, self).save(*args, **kwargs)


# import signals so they load on django load
from glynt.apps.project.signals import save_project_comment_signal
