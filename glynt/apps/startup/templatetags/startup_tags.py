# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def as_percentage_of(part, whole):
    part = (int(part)) + 1
    whole = (int(whole))
    try:
        return "%d%%" % (float(part) / float(whole) * 100)
    except (ValueError, ZeroDivisionError):
        return ""