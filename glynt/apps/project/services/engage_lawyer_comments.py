# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from threadedcomments.models import ThreadedComment

import logging
logger = logging.getLogger('lawpal.services')


class EngageLawyerCommentsMoveService(object):
    """
    Service to move the comment objects associated with
    a ProjectLawyer object to the Project discussion.
    """
    def __init__(self, project_lawyer_join):
        self.join = project_lawyer_join
        self.join_contenttype = ContentType.objects.get_for_model(project_lawyer_join)

        self.project = project_lawyer_join.project
        self.project_contenttype = ContentType.objects.get_for_model(self.project)

        self.comments = ThreadedComment.objects.filter(content_type=self.join_contenttype, object_pk=self.join.pk)

    def process(self):
        if len(self.comments) > 0:
            self.comments.update(content_type=self.project_contenttype, object_pk=self.project.pk)
