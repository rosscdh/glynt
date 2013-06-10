# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from glynt.apps.engage import ENGAGEMENT_STATUS


class DefaultEngageManager(models.Manager):
    def founder_lawyer_engagement(self, founder, lawyer):
        try:
            # has a previous engagement with this lawyer
            return self.get(lawyer=lawyer, founder=founder)
        except ObjectDoesNotExist:
            # @BUSINESSRULE
            # does not have a previous engagement with this lawyer so look for this startups previous
            # engagement and use that as a template
            try:
                return self.filter(founder=founder).order_by('-id')[0]
            except IndexError:
                return None

    def new(self, founder, lawyer):
        #get any new engagements between the founder and lawyer
        return self.filter(lawyer=lawyer, founder=founder, engagement_status=ENGAGEMENT_STATUS.new)

    def open(self, founder, lawyer):
        #filter out any closed engagements between the founder and lawyer
        return self.filter(lawyer=lawyer, founder=founder).exclude(engagement_status=ENGAGEMENT_STATUS.closed)

    def closed(self, founder, lawyer):
        #get any closed engagements between the founder and lawyer
        return self.filter(lawyer=lawyer, founder=founder, engagement_status=ENGAGEMENT_STATUS.closed)