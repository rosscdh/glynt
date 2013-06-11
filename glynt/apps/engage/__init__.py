# -*- coding: utf-8 -*-
import hashlib
import datetime
from glynt.apps.utils import get_namedtuple_choices


ENGAGEMENT_STATUS = get_namedtuple_choices('ENGAGEMENT_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'closed', 'Closed'),
))

from glynt.apps.utils import get_namedtuple_choices


ENGAGEMENT_STATUS = get_namedtuple_choices('ENGAGEMENT_STATUS', (
    (0, 'new', 'New'),
    (1, 'open', 'Open'),
    (2, 'closed', 'Closed'),
))


def generate_engagement_slug(engagement):
    """ Generate the unique slug for this model """
    hash_val = u'%s-%s' % (engagement.pk, datetime.datetime.utcnow())
    h = hashlib.sha1(hash_val)
    return h.hexdigest()
