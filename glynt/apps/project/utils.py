# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

PROJECT_CONTENT_TYPE = ContentType.objects.filter(model='project')