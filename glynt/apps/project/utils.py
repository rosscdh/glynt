# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

PROJECT_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="project")
PROJECTLAWYER_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="projectlawyer")