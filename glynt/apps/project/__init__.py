# -*- coding: utf-8 -*-
from django import dispatch
from django.contrib.contenttypes.models import ContentType

from glynt.apps.utils import get_namedtuple_choices

PROJECT_STATUS = get_namedtuple_choices('PROJECT_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'closed', 'Closed'),
))

PROJECT_LAWYER_STATUS = get_namedtuple_choices('PROJECT_LAWYER_STATUS', (
    (0, 'potential', 'Proposed'),
    (1, 'assigned', 'Engaged'),
    (2, 'rejected', 'Unsuccessful'),
))

PROJECT_CREATED = dispatch.Signal(providing_args=["created", "instance"])
PROJECT_PROFILE_IS_COMPLETE = dispatch.Signal(providing_args=["instance"])

PROJECT_CATEGORY_SORT_UPDATED = dispatch.Signal(providing_args=["instance", "user", "categories"])

from .signals import (on_project_created, on_save_ensure_user_in_participants, 
                      on_lawyer_assigned,
                      lawyer_on_save_ensure_participants,
                      lawyer_on_delete_ensure_participants,)