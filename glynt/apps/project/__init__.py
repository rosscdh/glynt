# -*- coding: utf-8 -*-
from glynt.apps.utils import get_namedtuple_choices


PROJECT_STATUS = get_namedtuple_choices('PROJECT_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'closed', 'Closed'),
))

PROJECT_LAWYER_STATUS = get_namedtuple_choices('PROJECT_LAWYER_STATUS', (
    (0, 'potential', 'Potential'),
    (1, 'assigned', 'Assigned'),
    (2, 'rejected', 'Rejected'),
))
