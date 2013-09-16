# -*- coding: utf-8 -*-
from glynt.apps.default.bunches import BaseDataBagBunch
from bunch import Bunch

import shortuuid

import logging
logger = logging.getLogger('lawpal.services')


class ProjectIntakeBunch(BaseDataBagBunch):
    """
    Bunch is used to Save Intake form data to the appropriate
    data_bag (project.data)
    """


class ProjectIntakeFormIsCompleteBunch(Bunch):
    """
    Bunch is used to test if the project profile has been completed
    integrated in views and in the middleware
    """
    errors = None
    project = None
    company = None

    def __init__(self, project):
        self.project = project
        self.company = self.project.company
        return super(ProjectIntakeFormIsCompleteBunch, self).__init__()

    def slug(self, **kwargs):
        name = str(self.project.pk) + '-' + str(self.company.pk)

        #if len(kwargs.keys()) > 0:
        #    name = '{name}{extra}'.format(name=name, extra='-'.join([i for i in kwargs.values()]))

        return shortuuid.uuid(name=name)

    def is_valid(self):
        is_valid = self.project.data.get('profile_is_complete', False)

        if not is_valid:
            self.errors = ['Project Profile has not been completed']

        return is_valid
