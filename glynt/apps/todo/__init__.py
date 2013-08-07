# coding: utf-8
from glynt.apps.utils import get_namedtuple_choices


TODO_STATUS = get_namedtuple_choices('TODO_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'pending', 'Pending'),
    (3, 'resolved', 'Resolved'),
    (4, 'closed', 'Closed'),
))