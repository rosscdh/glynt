# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType


def _PROJECT_CONTENT_TYPE():
    return ContentType.objects.get(app_label="project", model="project")


def _PROJECTLAWYER_CONTENT_TYPE():
    return ContentType.objects.get(app_label="project", model="projectlawyer")
