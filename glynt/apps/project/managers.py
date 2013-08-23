# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from . import PROJECT_STATUS, PROJECT_LAWYER_STATUS


class DefaultProjectManager(models.Manager):
    def for_user(self, user):
        """ get projects for a user class"""
        fltr = {}
        if user.profile.is_customer:
            fltr.update({'customer': user})
        elif user.profile.is_lawyer:
            fltr.update({'lawyer': user})
        else:
            raise Exception('Could not identify user class')

        return self.filter(**fltr)

    def current(self, **kwargs):
        return self.filter(status__in=[PROJECT_STATUS.open, PROJECT_STATUS.new]).filter(**kwargs)

    def new(self, **kwargs):
        return self.filter(status=PROJECT_STATUS.new).filter(**kwargs)

    def open(self, **kwargs):
        return self.filter(status=PROJECT_STATUS.open).filter(**kwargs)

    def closed(self, **kwargs):
        return self.filter(status=PROJECT_STATUS.closed).filter(**kwargs)

    def historic(self, customer, lawyer):
        """ @BUSINESSRULE Method to get a Customers current Project
        with a specified lawyer, if none Found then try for the last that
        the Customer created; as we assume he still has the same requirements.
        If his requirements have changed, then the next time he contacts a
        lawyer the process repeats"""
        try:
            # has a previous project with this lawyer
            return self.get(lawyer=lawyer, customer=customer).order_by('-id')
        except ObjectDoesNotExist:
            # @BUSINESSRULE
            # does not have a previous project with this lawyer so look for this companies previous
            # project and use that as a template
            try:
                return self.filter(customer=customer).order_by('-id')[0]
            except IndexError:
                return None


class ProjectLawyerManager(models.Manager):
    def potential(self, **kwargs):
        return self.filter(status=PROJECT_LAWYER_STATUS.potential).filter(**kwargs)

    def assigned(self, **kwargs):
        return self.filter(status=PROJECT_LAWYER_STATUS.assigned).filter(**kwargs)

    def rejected(self, **kwargs):
        return self.filter(status=PROJECT_LAWYER_STATUS.rejected).filter(**kwargs)
