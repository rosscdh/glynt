# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from glynt.apps.project import PROJECT_STATUS


class DefaultProjectManager(models.Manager):
    def for_user(self, user):
        """ get projects for a user class"""
        fltr = {}
        if user.profile.is_founder:
            fltr.update({'founder': user})
        elif user.profile.is_lawyer:
            fltr.update({'lawyer': user})
        else:
            raise Exception('Could not identify user class')

        return self.filter(**fltr)

    def open(self, **kwargs):
        return self.filter(project_status=PROJECT_STATUS.open).filter(**kwargs)

    def closed(self, **kwargs):
        return self.filter(project_status=PROJECT_STATUS.closed).filter(**kwargs)

    def new(self, **kwargs):
        return self.filter(project_status=PROJECT_STATUS.new).filter(**kwargs)

    def historic(self, founder, lawyer):
        """ @BUSINESSRULE Method to get a Founders current Project 
        with a specified lawyer, if none Found then try for the last that
        the Founder created; as we assume he still has the same requirements.
        If his requirements have changed, then the next time he contacts a 
        lawyer the process repeats"""
        try:
            # has a previous project with this lawyer
            return self.get(lawyer=lawyer, founder=founder).order_by('-id')
        except ObjectDoesNotExist:
            # @BUSINESSRULE
            # does not have a previous project with this lawyer so look for this companies previous
            # project and use that as a template
            try:
                return self.filter(founder=founder).order_by('-id')[0]
            except IndexError:
                return None

    def new(self, founder, lawyer):
        #get any new projects between the founder and lawyer
        return self.filter(lawyer=lawyer, founder=founder, project_status=PROJECT_STATUS.new)

    def open(self, founder, lawyer):
        #filter out any closed projects between the founder and lawyer
        return self.filter(lawyer=lawyer, founder=founder).exclude(project_status=PROJECT_STATUS.closed)

    def closed(self, founder, lawyer):
        #get any closed projects between the founder and lawyer
        return self.filter(lawyer=lawyer, founder=founder, project_status=PROJECT_STATUS.closed)
