# -*- coding: utf-8 -*-
from bunch import Bunch

import hashlib
import json

import logging
logger = logging.getLogger('lawpal.services')


class ProjectIntakeFormIsCompleteBunch(Bunch):
    errors = None
    project = None
    company = None

    def __init__(self, project):
        self.project = project
        self.company = self.project.company
        return super(ProjectIntakeFormIsCompleteBunch, self).__init__()

    def slug(self, **kwargs):
        m = hashlib.sha1()
        m.update(str(self.project.pk) + '-' + str(self.company.pk))
        if len(kwargs.keys()) > 0:
            m.update(json.dumps(kwargs))
        return m.hexdigest()

    def is_valid(self):
        is_valid = self.project.data.get('profile_is_complete', False)

        if not is_valid:
            self.errors = ['Project Profile has not been completed']

        return is_valid