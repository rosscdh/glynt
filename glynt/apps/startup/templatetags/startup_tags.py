# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def as_percentage_of(part, whole):
    #whole = int(float(whole))
    try:
        return "%d%%" % (int(float(part)) / int(float(whole)) * 100)
    except (ValueError, ZeroDivisionError):
        print 'yup'
        return ""