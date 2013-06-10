# -*- coding: utf-8 -*-
import hashlib
import datetime


def generate_engagement_slug(engagement):
    """ Generate the unique slug for this model """
    hash_val = u'%s-%s' % (engagement.pk, datetime.datetime.utcnow())
    h = hashlib.sha1(hash_val)
    return h.hexdigest()