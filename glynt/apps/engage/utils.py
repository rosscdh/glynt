# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

ENGAGEMENT_CONTENT_TYPE = ContentType.objects.filter(model='engagement')