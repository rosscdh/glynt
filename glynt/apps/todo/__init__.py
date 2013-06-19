# coding: utf-8
from glynt.apps.utils import get_namedtuple_choices


TODO_STATUS = get_namedtuple_choices('TODO_STATUS', (
    (0, 'open', 'Open'),
    (1, 'done', 'Done'),
    (2, 'in_progress', 'In-Progress'),
))