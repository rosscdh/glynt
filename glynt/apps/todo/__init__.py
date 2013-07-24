# coding: utf-8
from glynt.apps.utils import get_namedtuple_choices


TODO_STATUS = get_namedtuple_choices('TODO_STATUS', (
    (0, 'unassigned', 'Unassigned'),
    (1, 'assigned', 'Assigned'),
    (2, 'closed', 'Closed'),
))