# -*- coding: utf-8 -*-
from django.db import models

from glynt.apps.project.models import Project
from glynt.apps.lawyer.models import Lawyer

from glynt.apps.project.managers import ProjectLawyerManager
from glynt.apps.project import PROJECT_LAWYER_STATUS


class ProjectLawyer(models.Model):
    """
    The customised variation of a generic m2m model
    msut be named ProjectLawyer(s) <-- this is not noraml for django
    """
    LAWYER_STATUS = PROJECT_LAWYER_STATUS

    project = models.ForeignKey(Project)
    lawyer = models.ForeignKey(Lawyer)
    status = models.IntegerField(choices=LAWYER_STATUS.get_choices(),
                                 default=LAWYER_STATUS.potential,
                                 db_index=True)

    objects = ProjectLawyerManager()

    class Meta:
        db_table = 'project_project_lawyer'

    @property
    def display_status(self):
        return self.LAWYER_STATUS.get_desc_by_value(self.status)
