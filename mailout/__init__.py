# -*- coding: utf-8 -*-
"""
"""
from django.conf import settings

ABRIDGE_API_URL = getattr(settings, 'ABRIDGE_API_URL', 'http://localhost:8001/')
ABRIDGE_PROJECT = getattr(settings, 'ABRIDGE_PROJECT', None)

ABRIDGE_ACCESS_KEY_ID = getattr(settings, 'ABRIDGE_ACCESS_KEY_ID', None)
ABRIDGE_SECRET_ACCESS_KEY = getattr(settings, 'ABRIDGE_SECRET_ACCESS_KEY', None)
ABRIDGE_USERNAME = getattr(settings, 'ABRIDGE_USERNAME', None)
ABRIDGE_PASSWORD = getattr(settings, 'ABRIDGE_PASSWORD', None)


if ABRIDGE_ACCESS_KEY_ID is None:
    raise Exception("You must specify a ABRIDGE_ACCESS_KEY_ID in your settings.py")
if ABRIDGE_SECRET_ACCESS_KEY is None:
    raise Exception("You must specify a ABRIDGE_SECRET_ACCESS_KEY in your settings.py")
if ABRIDGE_PROJECT is None:
    raise Exception("You must specify a ABRIDGE_PROJECT in your settings.py")
if ABRIDGE_USERNAME is None:
    raise Exception("You must specify a ABRIDGE_USERNAME in your settings.py")
if ABRIDGE_PASSWORD is None:
    raise Exception("You must specify a ABRIDGE_PASSWORD in your settings.py")


from mailout.services import AbridgeMailoutService