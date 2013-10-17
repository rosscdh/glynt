# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from bunch import Bunch

try:
    _PROJECT_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="project")
    _PROJECTLAWYER_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="projectlawyer")
except:
    # for when there are no contenttype obejcts yet
    # take a wile guess based on local
    _PROJECT_CONTENT_TYPE = Bunch(pk=14, app_label="project", model="project")
    _PROJECTLAWYER_CONTENT_TYPE = Bunch(pk=15, app_label="project", model="projectlawyer")