# -*- coding: UTF-8 -*-
from django.db import models


class LawyerManager(models.Manager):
    def approved(self):
        # exclude users who have not set their password
        return super(LawyerManager, self).get_query_set() \
                    .select_related('user', 'user__profile') \
                    .exclude(is_active=False) \
                    .filter(user__is_active=True) \
                    .prefetch_related('user', 'firm_lawyers')