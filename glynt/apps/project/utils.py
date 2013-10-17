# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType


try:
    _PROJECT_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="project")
    _PROJECTLAWYER_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="projectlawyer")
except:
    # for when there are no contenttype obejcts yet
    pass
