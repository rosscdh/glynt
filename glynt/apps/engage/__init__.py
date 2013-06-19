# -*- coding: utf-8 -*-
from glynt.apps.utils import get_namedtuple_choices

ENGAGEMENT_STATUS = get_namedtuple_choices('ENGAGEMENT_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'closed', 'Closed'),
))
