# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from glynt.apps.engage import ENGAGEMENT_STATUS


class DefaultEngagementManager(models.Manager):
    def open(self, **kwargs):
        self.filter(engagement_status=ENGAGEMENT_STATUS.open).filter(**kwargs)

    def closed(self, **kwargs):
        self.filter(engagement_status=ENGAGEMENT_STATUS.closed).filter(**kwargs)

    def new(self, **kwargs):
        self.filter(engagement_status=ENGAGEMENT_STATUS.new).filter(**kwargs)

    def historic(self, founder, lawyer):
        """ @BUSINESSRULE Method to get a Founders current Engagement 
        with a specified lawyer, if none Found then try for the last that
        the Founder created; as we assume he still has the same requirements.
        If his requirements have changed, then the next time he contacts a 
        lawyer the process repeats"""
        try:
            # has a previous engagement with this lawyer
            return self.get(lawyer=lawyer, founder=founder).order_by('-id')
        except ObjectDoesNotExist:
            # @BUSINESSRULE
            # does not have a previous engagement with this lawyer so look for this startups previous
            # engagement and use that as a template
            try:
                return self.filter(founder=founder).order_by('-id')[0]
            except IndexError:
                return None
