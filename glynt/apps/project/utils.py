# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

import logging
logger = logging.getLogger('django.request')


try:
    _PROJECT_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="project")
    _PROJECTLAWYER_CONTENT_TYPE = ContentType.objects.get(app_label="project", model="projectlawyer")
except:
    # for when there are no contenttype obejcts yet
    # take a wile guess based on local
    # @BUSINESS_RULE these pk values are based on the preview and live values
    # if you need it for dev look up your local dev shell_plus
    # >>> ContentType.objects.filter(app_label="project", model="project")[0].pk
    # >>> ContentType.objects.filter(app_label="project", model="projectlawyer")[0].pk
    logger.critical('ContentType is being set manually in project.utils should not happen for web requests, but can for cli events')
    _PROJECT_CONTENT_TYPE = ContentType(pk=15, app_label="project", model="project")
    _PROJECTLAWYER_CONTENT_TYPE = ContentType(pk=16, app_label="project", model="projectlawyer")