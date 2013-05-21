# -*- coding: UTF-8 -*-
from django.db import models


class DefaultLawyerManager(models.Manager):
    pass

class ApprovedLawyerManager(models.Manager):
    """ Lists of Lawyers that have been approved and are valid """
    def get_query_set(self):
        # exclude users who have not set their password
        return super(ApprovedLawyerManager, self).get_query_set() \
                    .select_related('user', 'user__profile') \
                    .exclude(is_active=False) \
                    .filter(user__is_active=True) \
                    .prefetch_related('user', 'firm_lawyers')